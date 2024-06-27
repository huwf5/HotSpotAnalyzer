import { Messages } from "@/api/interface";

export function comp(a: Messages.ResMessage, b: Messages.ResMessage) {
  if (a.is_starred !== b.is_starred) return a.is_starred ? -1 : 1;
  else if (a.is_read !== b.is_read) return a.is_read ? -1 : 1;
  else if (a.type !== b.type) return a.type > b.type ? -1 : 1;
  else return new Date(a.message.created_at).getTime() > new Date(b.message.created_at).getTime() ? -1 : 1;
}
