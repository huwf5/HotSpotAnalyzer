import { Messages } from "@/api/interface";

export function comp(a: Messages.Message, b: Messages.Message) {
  if (a.starred !== b.starred) return a.starred ? -1 : 1;
  else if (a.unread !== b.unread) return a.unread ? -1 : 1;
  else if (a.type !== b.type) return a.type > b.type ? -1 : 1;
  else return a.time > b.time ? -1 : 1;
}
