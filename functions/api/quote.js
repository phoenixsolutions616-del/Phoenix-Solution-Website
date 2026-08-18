/**
 * Phoenix Solutions - quote form handler (Cloudflare Pages Function)
 *
 * Receives the quote form as multipart/form-data, then emails it to the
 * office inbox via the Resend API (https://resend.com).
 *
 * Required environment variables (set in Cloudflare Pages > Settings >
 * Variables and Secrets):
 *   RESEND_API_KEY  - secret. API key from resend.com with "Sending" access
 *   TO_EMAIL        - optional. Defaults to info@phoenixsolutions.com
 *   FROM_EMAIL      - optional. Defaults to quotes@phoenix-solutionsuk.com
 *                     (the domain part must be verified in Resend)
 */

const DEFAULT_TO = "info@phoenixsolutions.com";
const DEFAULT_FROM = "Phoenix Solutions Website <quotes@phoenix-solutionsuk.com>";
const MAX_FILES = 6;
const MAX_TOTAL_BYTES = 15 * 1024 * 1024; // 15 MB across all attachments

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.RESEND_API_KEY) {
    return json(503, {
      ok: false,
      error: "Email sending is not configured yet (missing RESEND_API_KEY).",
    });
  }

  let form;
  try {
    form = await request.formData();
  } catch (e) {
    return json(400, { ok: false, error: "Could not read form data." });
  }

  // Honeypot: real users never fill this hidden field.
  if ((form.get("company") || "").toString().trim() !== "") {
    // Pretend success so bots learn nothing.
    return json(200, { ok: true });
  }

  const field = (n) => (form.get(n) || "").toString().trim();

  const name = field("name");
  const email = field("email");
  if (!name || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json(400, { ok: false, error: "Please provide a valid name and email address." });
  }

  const data = {
    services: field("services") || "Not specified",
    property_type: field("property_type"),
    role: field("role"),
    postcode: field("postcode"),
    timing: field("timing"),
    details: field("details"),
    name,
    email,
    phone: field("phone"),
    contact_pref: field("contact_pref"),
  };

  // ---- attachments -------------------------------------------------------
  const attachments = [];
  let totalBytes = 0;
  const files = form.getAll("files").filter((f) => typeof f === "object" && f && f.size > 0);
  for (const file of files.slice(0, MAX_FILES)) {
    totalBytes += file.size;
    if (totalBytes > MAX_TOTAL_BYTES) break; // silently skip the rest, note added below
    const buf = await file.arrayBuffer();
    attachments.push({ filename: sanitiseFilename(file.name), content: toBase64(buf) });
  }
  const skipped = files.length - attachments.length;

  // ---- email body --------------------------------------------------------
  const subject = `Quote request - ${data.services} - ${name}${data.postcode ? " (" + data.postcode + ")" : ""}`;

  const rows = [
    ["Services", data.services],
    ["Name", name],
    ["Email", email],
    ["Phone", data.phone || "Not given"],
    ["Preferred contact", data.contact_pref || "No preference"],
    ["Property type", data.property_type || "Not given"],
    ["Role", data.role || "Not given"],
    ["Postcode", data.postcode || "Not given"],
    ["Timing", data.timing || "Not given"],
  ];

  const text =
    rows.map(([k, v]) => `${k}: ${v}`).join("\n") +
    `\n\nJob details:\n${data.details || "(none provided)"}` +
    (attachments.length ? `\n\nAttachments: ${attachments.length} file(s)` : "") +
    (skipped > 0 ? `\n(${skipped} file(s) were skipped for exceeding the size limit)` : "");

  const html = `
  <div style="font-family:Arial,Helvetica,sans-serif;color:#1A1A1A;max-width:640px">
    <h2 style="color:#FF6A00;margin:0 0 4px">New quote request</h2>
    <p style="margin:0 0 18px;color:#555">Submitted via phoenix-solutionsuk.com</p>
    <table cellpadding="7" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:14px">
      ${rows
        .map(
          ([k, v]) =>
            `<tr><td style="border:1px solid #E6E6E6;background:#F7F7F7;font-weight:bold;width:170px">${esc(k)}</td>` +
            `<td style="border:1px solid #E6E6E6">${esc(v)}</td></tr>`
        )
        .join("")}
    </table>
    <h3 style="margin:20px 0 6px">Job details</h3>
    <p style="white-space:pre-wrap;font-size:14px;border-left:4px solid #FF6A00;padding-left:12px;margin:0">${esc(
      data.details || "(none provided)"
    )}</p>
    ${skipped > 0 ? `<p style="color:#a33">${skipped} attachment(s) were skipped for exceeding the 15&nbsp;MB limit.</p>` : ""}
  </div>`;

  // ---- send via Resend ---------------------------------------------------
  const payload = {
    from: env.FROM_EMAIL || DEFAULT_FROM,
    to: [env.TO_EMAIL || DEFAULT_TO],
    reply_to: `${name} <${email}>`,
    subject,
    html,
    text,
  };
  if (attachments.length) payload.attachments = attachments;

  const resp = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!resp.ok) {
    const detail = await resp.text().catch(() => "");
    console.error("Resend error", resp.status, detail);
    return json(502, { ok: false, error: "The email service rejected the message. Please try again or call us." });
  }

  return json(200, { ok: true });
}

// Anything other than POST gets a polite 405.
export async function onRequest(context) {
  if (context.request.method === "POST") return onRequestPost(context);
  return json(405, { ok: false, error: "Method not allowed." });
}

/* ---------------- helpers ---------------- */

function json(status, obj) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function sanitiseFilename(name) {
  return String(name || "attachment").replace(/[^\w.\- ()]/g, "_").slice(0, 120);
}

function toBase64(arrayBuffer) {
  const bytes = new Uint8Array(arrayBuffer);
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}
