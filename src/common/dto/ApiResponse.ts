import { ErrorResponse } from "./ErrorResponse";

export interface PaginationMeta {
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

//API response
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ErrorResponse;
  meta?: PaginationMeta;
  correlationId?: string;
}

export function ok<T>(
  data: T,
  meta?: PaginationMeta,
  correlationId?: string
): ApiResponse<T> {
  return {
    success: true,
    data,
    meta,
    correlationId,
  };
}

export function fail<T = never>(
  error: ErrorResponse,
  correlationId?: string
): ApiResponse<T> {
  return {
    success: false,
    error,
    correlationId,
  };
}
