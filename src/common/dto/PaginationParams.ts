export interface PaginationParams {
  page?: number;
  pageSize?: number;
}

export const DEFAULT_PAGE = 1;
export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;

export function normalizePagination(
  params: PaginationParams
): Required<PaginationParams> {
  const page =
    params.page && params.page > 0 ? Math.floor(params.page) : DEFAULT_PAGE;

  let pageSize =
    params.pageSize && params.pageSize > 0
      ? Math.floor(params.pageSize)
      : DEFAULT_PAGE_SIZE;

  if (pageSize > MAX_PAGE_SIZE) {
    pageSize = MAX_PAGE_SIZE;
  }

  return { page, pageSize };
}
