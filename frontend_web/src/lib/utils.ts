import { VITE_DEFAULT_PORT } from "@/constants/dev";

export function getApiPort() {
  return window.ENV?.API_PORT;
}

export function getBaseUrl() {
  let basename = window.ENV?.BASE_PATH;
  // Adjust API URL based on the environment
  const pathname: string = window.location.pathname;

  if (
    pathname?.includes("notebook-sessions") &&
    pathname?.includes(`/${VITE_DEFAULT_PORT}/`)
  ) {
    // ex:. /notebook-sessions/{id}/ports/5137/
    basename = import.meta.env.BASE_URL;
  }

  return basename ? basename : "/";
}

export function getApiUrl() {
  return `${window.location.origin}${getBaseUrl()}api`;
}
