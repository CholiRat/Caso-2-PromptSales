// src/common/exceptions/ValidationException.ts
import { AppException } from "./AppException";

export interface ValidationErrorItem {
  field: string;
  message: string;
}

export class ValidationException extends AppException {
  public readonly errors: ValidationErrorItem[];

  constructor(errors: ValidationErrorItem[]) {
    super("Validation failed", 400, "VALIDATION_ERROR", errors);
    this.errors = errors;
  }
}
