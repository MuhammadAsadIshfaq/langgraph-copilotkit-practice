import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export const truncateUrl = (url, maxLength = 40) => {
  if (!url) return "";
  if (url.length <= maxLength) return url;
  return url.substring(0, maxLength - 3) + "...";
};
