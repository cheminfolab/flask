import { apiClient } from "@/lib/api"

/**
 * Kept for existing callers. Returns the shared, stable API client (see
 * `@/lib/api`): authentication and token refresh are handled there for
 * every request, so there is nothing per-component to configure.
 */
const useAxios = () => apiClient

export default useAxios
