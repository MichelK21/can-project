import { UserManager, WebStorageStateStore } from "oidc-client-ts";

const authority = "https://alszzhqan.trial-accounts.ondemand.com";

export const userManager = new UserManager({
  authority,
  client_id: "6247cb12-0744-4d0c-9311-d49bd8f639cf",

  redirect_uri: "http://localhost:5173/auth/callback",
  post_logout_redirect_uri: "http://localhost:5173/",

  response_type: "code",
  scope: "openid profile email",

  automaticSilentRenew: true,
  loadUserInfo: true,

  userStore: new WebStorageStateStore({
    store: window.sessionStorage,
  }),
});
