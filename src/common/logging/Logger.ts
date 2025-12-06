export type LogLevel = "debug" | "info" | "warn" | "error";

export interface LoggerOptions {
  serviceName: string;
  level?: LogLevel;
}

const levelsOrder: LogLevel[] = ["debug", "info", "warn", "error"];

export class Logger {
  private readonly serviceName: string;
  private readonly level: LogLevel;

  constructor(options: LoggerOptions) {
    this.serviceName = options.serviceName;
    this.level = options.level ?? "info";
  }

  private shouldLog(level: LogLevel): boolean {
    return (
      levelsOrder.indexOf(level) >= levelsOrder.indexOf(this.level)
    );
  }

  private format(
    level: LogLevel,
    message: string,
    meta?: unknown
  ): string {
    const ts = new Date().toISOString();
    const base = `[${ts}] [${this.serviceName}] [${level.toUpperCase()}] ${message}`;
    return meta ? `${base} | ${JSON.stringify(meta)}` : base;
  }

  debug(message: string, meta?: unknown): void {
    if (this.shouldLog("debug")) {
      console.debug(this.format("debug", message, meta));
    }
  }

  info(message: string, meta?: unknown): void {
    if (this.shouldLog("info")) {
      console.info(this.format("info", message, meta));
    }
  }

  warn(message: string, meta?: unknown): void {
    if (this.shouldLog("warn")) {
      console.warn(this.format("warn", message, meta));
    }
  }

  error(message: string, meta?: unknown): void {
    if (this.shouldLog("error")) {
      console.error(this.format("error", message, meta));
    }
  }
}

export const defaultLogger = new Logger({ serviceName: "PromptSales" });
