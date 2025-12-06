import { Logger } from "./Logger";

export interface AuditEvent {
  action: string;
  entity: string;
  entityId?: string;
  userId?: string;
  correlationId?: string;
  metadata?: Record<string, unknown>;
}

/**
 * Very simple audit logger. In real life this would go to a dedicated DB / topic.
 */
export class AuditLogger {
  private readonly logger: Logger;

  constructor(serviceName = "Audit") {
    this.logger = new Logger({ serviceName, level: "info" });
  }

  log(event: AuditEvent): void {
    this.logger.info(
      `AUDIT ${event.action} ${event.entity}${
        event.entityId ? `#${event.entityId}` : ""
      }`,
      event
    );
  }
}

export const auditLogger = new AuditLogger();
