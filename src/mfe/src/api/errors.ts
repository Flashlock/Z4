export class ApiError extends Error {
  readonly status: number;
  readonly userMessage: string;
  readonly detail: unknown;

  constructor(status: number, userMessage: string, detail?: unknown) {
    super(userMessage);
    this.name = "ApiError";
    this.status = status;
    this.userMessage = userMessage;
    this.detail = detail;
  }
}

function formatDetail(detail: unknown): string | null {
  if (detail == null) return null;
  if (typeof detail === "string" && detail.trim()) return detail.trim();
  if (typeof detail === "object") {
    const obj = detail as Record<string, unknown>;
    const errorName = typeof obj.error === "string" ? obj.error : null;
    const message = typeof obj.message === "string" ? obj.message : null;
    const conflicts = Array.isArray(obj.conflicts)
      ? obj.conflicts.filter((c): c is string => typeof c === "string")
      : null;
    const nestedDetail = obj.detail;
    let nested: string | null = null;
    if (typeof nestedDetail === "string") nested = nestedDetail;
    else if (nestedDetail && typeof nestedDetail === "object") {
      const inner = nestedDetail as Record<string, unknown>;
      if (typeof inner.message === "string") {
        nested = inner.message;
        if (Array.isArray(inner.conflicts)) {
          const lines = inner.conflicts.filter((c): c is string => typeof c === "string");
          if (lines.length) nested += "\n" + lines.map((l) => `• ${l}`).join("\n");
        }
      } else {
        nested = JSON.stringify(nestedDetail, null, 2);
      }
    }
    const traceback = typeof obj.traceback === "string" ? obj.traceback : null;

    const parts: string[] = [];
    if (errorName && message) parts.push(`${errorName}: ${message}`);
    else if (message) parts.push(message);
    else if (errorName) parts.push(errorName);
    if (conflicts?.length) parts.push(conflicts.map((l) => `• ${l}`).join("\n"));
    if (nested) parts.push(nested);

    if (traceback) parts.push(traceback.trim());
    if (parts.length) return parts.join("\n\n");

    try {
      return JSON.stringify(detail, null, 2);
    } catch {
      return String(detail);
    }
  }
  return String(detail);
}

/** Build a straight, copyable error string from an HTTP failure. */
export function formatHttpError(status: number, url: string, body: unknown): string {
  const fromBody = formatDetail(body);
  const header = `HTTP ${status} ${url}`;
  return fromBody ? `${header}\n${fromBody}` : header;
}

export function toUserMessage(err: unknown, fallback: string): string {
  if (err instanceof ApiError) return err.userMessage;
  if (err instanceof TypeError) {
    return `${err.name}: ${err.message}\n(Network/fetch failure — is the agent reachable?)`;
  }
  if (err instanceof Error && err.message) return `${err.name}: ${err.message}`;
  return fallback;
}
