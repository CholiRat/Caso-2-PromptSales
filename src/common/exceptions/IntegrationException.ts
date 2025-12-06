// src/common/exceptions/IntegrationException.ts
import { AppException } from "./AppException";

export class IntegrationException extends AppException {
  public readonly targetSystem: string;

  constructor(
    targetSystem: string,
    message = "Error while calling external system",
    details?: unknown
  ) {
    super(message, 502, "INTEGRATION_ERROR", details);
    this.targetSystem = targetSystem;
  }
}
