# Plasma session components

These components target the **Plasma 5.27 interface contracts**. They remain experimental until isolated native greeter and desktop acceptance is complete. Plasma 6 session behavior remains unverified.

## Native contracts

- The lock screen starts a conversation through the supplied `authenticator.tryUnlock()`, passes responses through `respond()`, clears responses after submission, handles failure and further prompts, and requests exit only after `authenticator.unlocked` is true. The native greeter also checks this state. Missing authentication disables the input. The theme does not call PAM directly.
- Logout actions use `rebootRequested()`, `haltRequested()`, `suspendRequested(int)`, `logoutRequested()` and `cancelRequested()`. Host capability flags control availability. Escape and Cancel stop the countdown; the countdown performs the host-selected action rather than always logging out. Controls support keyboard activation and visible focus.
- The OSD accepts the host's `icon`, `osdValue`, `osdMaxValue`, `osdAdditionalText`, `showingProgress` and `timeout` properties. It supports text notices and percentages above 100. Text is rendered literally.

## Manual validation

Verify these experimental components in an isolated Plasma 5.27 session before use. Check authentication success and failure, password clearing, further prompts, keyboard focus, session cancellation, capability-dependent controls and OSD values. Native loading, authentication policy, multiple monitors and assistive technology require application-level acceptance. Repository checks do not exercise session behavior.

References: [Plasma 5.27 authenticator](https://invent.kde.org/plasma/kscreenlocker/-/blob/Plasma/5.27/greeter/pamauthenticator.h), [logout host](https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/5.27/logout-greeter/shutdowndlg.cpp), [OSD host](https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/5.27/shell/osd.cpp).
