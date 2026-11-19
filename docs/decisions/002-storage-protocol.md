# B0a storage capability protocol

Status: **Proposed protocol; overall NO-GO for product implementation or a target experiment.**
Date: 2026-11-19. GPT-6 Astra (`gpt-6-astra`) / OpenCode, registered ReleaseLens worker.
No capability test was executed. No eligible external target has been authorized or provisioned.

## Scope and evidence boundary

[Issue #12](https://github.com/Himanshu-singh04/releaselens/issues/12) preserves A1–A6 and the
original founder instruction: “ok then proceed with the further tasks”. This slice specifies
Store's proposed native interface, target eligibility and finite fault protocol. It does not
authorize an experiment, implementation, installation, account operation or storage change.
[B0 merge verification](https://github.com/Himanshu-singh04/releaselens/pull/11#issuecomment-7000315548)
records accepted research at `1bfa0576aabfbb17a9a625a513a1d7dea6079eb3`, conditional on validation.
The [B0 observations](001-runtime.md) remain historical evidence, not tested pins or M0 closure.

Authoritative obligations remain [R5/R7 and T-08/09](../testing.md), [private access and
pinned I/O](../operations.md), [RL-010/011/012](../product.md), [report persistence and
60-second bound](../evidence-contract.md), and the [SDD](../specs/001-mvp/solution-design.md).
No requirement or expected test outcome in those documents changes here. G-* below names
sub-obligations for traceability; F-* names proposed tests, not observed results.

Observed in B0a: clean fetched main at the assigned SHA; macOS 27.2.1/build 26B131;
SDK 27.2; targeted header declarations listed in S9; `diskutil info -plist
/Volumes/AIWorkspace` reports APFS/USB, external, `GlobalPermissionsEnabled=false`;
`mount` confirms `noowners`. No database/credential inspection. The encryption observation
in B0 was not re-established by this query (its queried `Encrypted` key was absent).
Worker history/OAuth placement remains the founder's choice; authenticated localhost access
and outside-Git storage do not prove filesystem confidentiality. Other-account access remains
untested, with no demonstrated credential read/exposure. Provisioning #9 is not storage acceptance.

## Failure model and unchanged acceptance

Proposed narrow profile: one nonprivileged writer, no concurrent owner edits, explicit regular
input files and a new generation under an owner-private parent, on one owner-enabled local
external APFS volume. Trust the OS/kernel and accurately reporting storage hardware for any
durability claim. Inputs were privately prepared; permissions cannot revoke previously issued
foreign descriptors or erase earlier disclosures. No adversarial root, same-UID process,
kernel compromise or stolen-drive confidentiality promise. Encryption alone would not enforce
mounted access control. The writer never repairs permissions or chooses a fallback destination.

Ordinary other accounts must be unable to read evidence or replace protected namespace entries.
Root-owned system ancestors may be traversable but not replaceable by ordinary accounts.
An authorized fault driver may nevertheless change ACLs/names or force detach to exercise R5/R7:
the privacy threat exclusion does **not** waive those explicit failure/no-success tests.
Hardware loss, process interruption and blocking syscalls remain in scope as faults.

An oracle checks both the process outcome and storage state. A successful *publication*
includes candidate pass/fail/unknown (SDD exits 0/1/3); an operational failure is exit 4,
fixed E_IO/E_LIMIT/E_INTERNAL Diagnostic, and no success-summary stdout. A killed process
has no normal exit/Diagnostic guarantee; the observer records its signal and absent summary.

| Guarantee | Exact unchanged obligation and assumptions | Acceptance oracle / proposed coverage | Verdict for next experiment |
| --- | --- | --- | --- |
| G1 private creation/access | R5: effective owner-private inputs/output; reject wrong owner, broad/inherited ACL, noowners, unsupported protection before evidence writes. Modes alone are insufficient. Ordinary-account promise under the stable-owner model above. | Empty objects precede evidence; kernel denies another ordinary account's open/traverse attempts; zero evidence bytes at any rejected preflight, unchanged inputs. F-01/02/03/09. | **GO-for-next-experiment in principle** for metadata/empty-ACL investigation only; enforcement and target eligibility unverified. |
| G2 no redirected I/O | R7: retain verified handles, no path reopens or fallback directories, no writes into local/replacement trees during input reads/writes/publication. | Operation trace names only retained fds and single-component children; replacement-tree sentinels unchanged, original input hashes unchanged. F-04–08/20. | **GO-for-next-experiment in principle** for descriptor observations; native/OS behavior untested. |
| G3 ACL drift rejection | R5 also requires ACL drift not to expose evidence or publish successfully. Checking before/after is sampling, not continuous protection against an owner changing permissions. | Controlled drift between checkpoints must cause no ordinary-account disclosure and no success; F-10 includes a counterexample to this protocol. | **NO-GO** for the unqualified temporal guarantee; C1/D1 below. |
| G4 continuous identity/loss rejection | R7: root/ancestor/volume substitution or loss throughout I/O and immediately around marker must fail without success. UUID identifies a volume, not an unrepeatable mount epoch. | Fault driver records event intervals independently; compare them with syscall/check/summary times, not only final tuples. F-04–08/21. | **NO-GO** for universal detection/no-success by sampled tuples; C2/D2. |
| G5 no overwrite | RL-011/contract: new generation and marker, existing generations never overwritten. Trust same-volume exclusive namespace operations; no owner interference. | Existing bytes/inodes unchanged on generation/file/marker collisions, including competing creators; E_IO, no summary. F-11/12. | **GO-for-next-experiment in principle** for exclusive-rename capability metadata; collision enforcement still untested. |
| G6 logical recovery integrity | RL-011: no apparently complete partial report. Accept only exact required files plus a valid last marker binding both byte hashes; a directory/name alone never proves completion. | Reader rejects missing/partial/mismatched marker or report, and retains valid hash-consistent output only as recovered integrity. F-13–19/23. | **GO-for-next-experiment in principle** for a later isolated recovery test; no conformance run here. |
| G7 acknowledged durable publication | Operations: flush complete bytes and required namespace metadata before summary; marker is not a disk-loss guarantee. SDD's fatal/deadline text additionally says no complete marker. | Independent observer sees acknowledgement only after all ordered flush/check returns; post-restart hashes survive under a documented device failure model. A valid unacknowledged marker cannot prove the prior caller saw success. F-14–19/21/22. | **NO-GO**: target flush semantics untested; unconditional marker absence on late failure conflicts with C3/D3. |
| G8 deadline | Contract: runtime independently enforces a 60-second comparison deadline, including I/O; E_LIMIT/exit 4, no complete marker in SDD. No source establishes a bounded syscall/termination time. | External monotonic observer measures from compare entry (before Store.prepare) through outcome and outstanding I/O; block a syscall over the boundary. No late marker/summary. F-22. | **NO-GO** for a hard wall-clock termination/no-late-publication guarantee; C4/D4. |
| G9 lifetime/cleanup | SDD: IoContext retains handles across stages and releases them on all exits; no borrowed-fd use after close. | Count opens/closes and ACL allocations/frees at every return; invalid fd reuse, leaks or pending post-timeout writes fail. F-20/22/24. | **GO-for-next-experiment in principle** on returning paths; **NO-GO** for bounded cleanup of blocked syscalls. |

“GO-for-next-experiment in principle” means a falsifiable, bounded question worth testing,
not a passing guarantee or authorization. **Overall NO-GO**: G3/G4/G7/G8 need explicit
requirement decisions or a different design; even the metadata-only experiment below needs
an authorized target and separate permission. M0 and B1 remain blocked.

## Counterexamples and separate founder decisions

These are reasoned schedules, not executed attacks or claims of observed exposure.

- **C1 / G3:** after the last empty-file ACL check, an owner adds a read ACE to that file,
  the writer fills the file, an ordinary account reads it, and the owner removes the ACE
  before the next check. A later rejection cannot undo disclosure. Stable-owner kernel
  permissions can protect G1, but sampling cannot guarantee G3 over this schedule.
  **D1 proposed, unaccepted:** explicitly limit confidentiality to no owner/privileged
  permission changes, and require fail-closed on *observed* drift. Keep owner-driven drift
  tests as limitation demonstrations, not passing confidentiality tests. Otherwise retain NO-GO.
- **C2 / G4:** check `(parent fd, entry dev/inode, volume UUID/fsid)`; rename an ancestor
  away, substitute another directory, restore the original before the next check. Retained
  fds still access the original tree and tuple checks can pass. Parent metadata/notifications
  can add evidence but no reviewed source supplies a lossless, atomic namespace-history fence.
  Stronger counterexample: all final checks return, then physical loss occurs before stdout
  acknowledgement. No userspace check can be atomic with both future media loss and caller
  observation. **D2 proposed, unaccepted:** keep unconditional no-redirection/no-fallback;
  define identity rejection as observed mismatches/syscall failures at enumerated checkpoints,
  and bound acknowledgement to the last successful checkpoint, not continuous availability.
  The current R7 no-success oracle remains required and would fail these counterexamples.
- **C3 / G7:** marker rename and directory flush succeed; a later privacy/mount check,
  deadline or close fails (or the process dies before stdout). The marker may already be
  durable. Deleting it cannot reliably reverse publication after device loss, and creates
  another flush/failure window. Adding a second marker only moves the window. **D3 proposed,
  unaccepted:** distinguish recovered, hash-consistent publication from observed caller success;
  permit a valid unacknowledged generation after late failure. Do not change the existing
  “no complete marker” error text or claim that this candidate satisfies it.
- **C4 / G8/G9:** a flush/rename enters the kernel just before 60 seconds and does not return
  by the deadline. A Python signal handler runs later; a watchdog's kill request has no reviewed
  maximum completion time or transactional rollback. An in-flight rename may commit before
  termination. Scheduler suspension alone can delay the caller past 60 seconds. **D4 proposed,
  unaccepted:** retain a 60-second monotonic decision budget, suppress new work/success when
  expiry is observed, and specify best-effort cancellation with separately measured cleanup
  latency and indeterminate publication. This relaxes a hard completion bound and therefore
  needs founder approval; another process does not silently solve it. Retain NO-GO if a hard
  bound plus zero late marker is essential.

## Minimal proposed Darwin ABI under Store

This is interface notation, not a header, compiled helper or product API. Python's `os`
dir_fd operations, fstat, read/write, close, fsync and `fcntl(F_FULLFSYNC)` already cover
traversal and flushing [S1/S6/S9]; do not duplicate them in C. The missing native surface is
four operations plus a version query. Bridge v1 targets arm64 Darwin, the inspected SDK ABI
and a separately verified OS/libc build only. It is not a portable FFI to arbitrary symbols.

| Proposed export / parameters | Exact operation and result |
| --- | --- |
| `uint32_t rl_store_abi(void)` | Returns 1. Loader rejects a missing symbol, different version/architecture, or unverified artifact before any product I/O. No lazy fallback to path-based commands. |
| `int32_t rl_mount_v1(int32_t fd, MountV1 *out, uint32_t out_bytes, ErrorV1 *err)` | `fstatfs(fd)`; copy signed 32-bit fsid pair and 32-bit native mount flags; classify exact f_fstypename `apfs` as 1, other as 0. No paths returned [S2/S9]. |
| `int32_t rl_volume_v1(int32_t root_fd, VolumeV1 *out, uint32_t out_bytes, ErrorV1 *err)` | `fgetattrlist` on retained volume-root descriptor; request returned-attribute set, volume UUID, capabilities/valid bits and supported/native attribute masks. Copy values only after length/mask validation below [S3/S9]. |
| `int32_t rl_acl_empty_v1(int32_t fd, uint32_t *empty, ErrorV1 *err)` | Obtain independent ACL via `acl_get_fd_np(fd, ACL_TYPE_EXTENDED)`; validate the returned ACL object, test FIRST_ENTRY, return empty=1 or 0; free ACL on every path. Never set an ACL or return its pointers [S4/S5/S9]. |
| `int32_t rl_publish_marker_v1(int32_t generation_fd, ErrorV1 *err)` | Exactly `renameatx_np(fd, ".completion.pending", fd, "completion.json", RENAME_EXCL)`; no arbitrary names/flags. Atomic exclusive namespace step only, not a flush or identity transaction [S7/S9]. |

**Layout/version rules:** C calling convention, fixed-width stdint scalars; no C enum, bool,
long, size_t, Darwin struct, pointer-bearing record or packed-struct cast crosses the boundary.
Pointers are only synchronous caller-provided buffers. All records use 4-byte alignment:

- `MountV1` (24 bytes): `uint32_t version=1, bytes=24; int32_t fsid[2];
  uint32_t mount_flags, fs_kind;` (offsets 0, 4, 8, 16, 20).
- `VolumeV1` (116 bytes): `uint32_t version=1, bytes=116; uint8_t uuid[16];
  uint32_t capabilities[4], capability_valid[4], returned[5], supported[5], native[5];`
  (offsets 0, 4, 8, 24, 40, 56, 76, 96). Five-group order is common/volume/directory/file/fork;
  capability order is FORMAT/INTERFACES/RESERVED1/RESERVED2. Copy UUID bytes without swapping.
- `ErrorV1` (16 bytes): `uint32_t version=1, bytes=16; int32_t os_errno; uint32_t stage;`
  (offsets 0, 4, 8, 12). Stage: 0 validation, 1 fstatfs, 2 fgetattrlist, 3 ACL retrieval,
  4 ACL validation, 5 ACL entry, 6 ACL free, 7 rename. Capture errno immediately, before cleanup.

Future builds must static-assert native `int` width and each layout/offset; the loader verifies
the matched bridge artifact/version. Caller initializes version/bytes; bridge checks exact
output sizes, nonnull buffers and fd >=0 (AT_FDCWD forbidden). Payload is cleared on entry;
on any nonzero status callers must ignore it. Error record is initialized even on success.
Null/invalid memory pointers violate the in-process caller contract; this is not a sandbox.
ABI changes require a new suffix/version, never reinterpret a v1 record.

Return `int32_t`: 0 OK, 1 BAD_ARGUMENT, 2 UNSUPPORTED, 3 SYSTEM_ERROR, 4 MALFORMED_RESULT,
5 COLLISION. Missing platform/API, ENOTSUP/EOPNOTSUPP => 2; rename EEXIST => 5; other native
failures (including EINTR, EINVAL, EBADF, EIO, ENOSPC) => 3, except the narrowly specified ACL
empty-list case below. Invalid lengths/masks => 4. No retry, repair, path reopen or error-text
allocation inside the bridge. Store maps failures to fixed Diagnostics/exit 4; errno/stage are
numeric investigation evidence, not raw paths or exception text in product output. A failed
mutating call does not establish absent on-disk effects; retain uncertainty for recovery.

**Interruption layers:** Python 3.14.10 documents that `os.open`, `os.read` and `os.write`
retry an interrupted syscall when the signal handler does not raise, rather than surface
`InterruptedError` (since Python 3.5; exact function references in S1). A raw native EINTR
therefore need not return control to Store's abort path or between-call deadline/identity
checks. Store adds no retry after a surfaced `OSError` (including `InterruptedError`);
the bridge's no-retry rule applies only to its own native calls that return an error,
mapping returned EINTR to SYSTEM_ERROR as above. It does not govern Python's implicit
retries or guarantee that a signal interrupts a native call. Raising in a Python signal
handler is not a safe lifetime/cancellation solution: exceptions may arrive after any
bytecode instruction and leave state inconsistent [S8]. Return-to-Python timing, signal/
exception behavior and descriptor cleanup need future target conformance validation;
G8/G9 hard-deadline/bounded-cleanup NO-GO remains unchanged. No signal test ran here.

**Descriptor/lifetime:** caller owns every descriptor, retains it in IoContext from prepare
through P6's final checks (or abort), and serializes calls/close. Bridge borrows only for the call, never
dups, retains, closes, changes offsets or transfers fds. All fds are O_CLOEXEC. IoContext keeps
the system anchor/parent chain, volume root, private parent, three input fds, generation and
output/marker fds; close exactly once in reverse acquisition order on returning paths. Close
failure is an error, not reason to retry a possibly reused number. ACL memory never outlives
the call; entry descriptors are borrowed from that ACL and never freed separately. No global
state, callbacks, background work or imported-data-selected symbols. P6 teardown precedes
stdout so close errors can suppress acknowledgement; it leaves no handle for a further P7
check and does not satisfy continuous binding through shutdown. That is part of G4's NO-GO,
not a change to the operations requirement. Kill/deadline cleanup is G9's gap.

**Volume decoding:** initialize native attrlist with bitmapcount=ATTR_BIT_MAP_COUNT, reserved=0,
commonattr=ATTR_CMN_RETURNED_ATTRS; volattr=ATTR_VOL_INFO | ATTR_VOL_UUID |
ATTR_VOL_CAPABILITIES | ATTR_VOL_ATTRIBUTES; other groups zero. Use FSOPT_REPORT_FULLSIZE |
FSOPT_PACK_INVAL_ATTRS [S3]. Native result is 4-byte-aligned: length, returned attribute_set_t,
vol_capabilities_attr_t, uuid_t, vol_attributes_attr_t, in documented attribute order (not the
bridge output order). Compute capacity from SDK types; validate full length equals the expected
fixed payload and fits the buffer before copying with alignment-safe operations. Require
returned UUID/capabilities/attributes bits; never accept packed placeholder zeros as values.
Require supported volattr bits for those requested payload attributes; nativeattr describes
native versus emulated support, not per-call validity. Preserve both masks. All-zero UUID is
unsupported. Require valid **and** enabled VOL_CAP_INT_EXTENDED_SECURITY and
VOL_CAP_INT_RENAME_EXCL; unknown capability is not false-but-safe. Require known/clear
VOL_CAP_FMT_NO_PERMISSIONS and VOL_CAP_FMT_VOL_GROUPS for this profile. Reject noowners,
nonlocal, read-only or non-APFS output, malformed masks and any later mismatch. These are separate
syscalls, not an atomic mount snapshot. Pair UUID/fsid with fstat dev/inode and retained
parent-entry checks; none is a unique mount-generation token. Do not reopen by UUID/path.

**ACL decoding:** reject any nonempty extended ACL, including deny-only/inherit-only entries,
instead of implementing allow/deny/group-membership precedence. NULL retrieval or failed
`acl_valid` is an error, never empty. Apple `acl_get_entry` returns **0 for an entry**;
unlike some POSIX ACL implementations, end-of-list is -1/EINVAL [S5]. On a fresh successful
ACL retrieval validated by `acl_valid`, FIRST_ENTRY -1/EINVAL is the proposed empty-list
interpretation supported by the pinned Apple source; other errors fail. Do not infer absence
from EINVAL on arbitrary calls. Verify empty/nonempty/error distinctions on the target libc
before use; source is not proof of the installed binary. Save an error before `acl_free`,
free once even after rejection, and report cleanup failure if it is the first error. This
minimal query inspects no principals and proves neither effective foreign-account access nor
continuous ACL stability; G1 still needs an independently authorized negative-access test.

**Simpler alternative:** Python dir_fd operations plus stdlib `os.link` could publish a
fully written temporary marker with no-clobber semantics, then unlink its temporary name.
That avoids the rename export but adds a two-name crash state and needs link/cleanup tests;
it still lacks Darwin ACL/mount/UUID validation and does not solve G3/G4/G7/G8. Pure stdlib
plus chmod/path-based diskutil/ls checks cannot meet the contract. A small C executable with
JSON IPC adds descriptor transfer and cancellation lifetimes without fixing the guarantees.
No simpler alternative identified satisfies the **whole** unchanged contract; the four-call
bridge is the smallest candidate for the chosen single-step marker protocol, not a GO claim.

## Proposed target and eligibility procedure

Target **T-EXT-APFS-1 is a specification, not a device selection**. Require a separately
authorized, existing owner-enabled external local APFS volume on the observed arm64 Mac;
no system/data volume group, network/cloud-backed tree, automount substitution, symlink,
nested mount or redirected home/temp/cache. Record exact OS/build, volume UUID, hardware/
USB controller and firmware, APFS case-sensitivity, mount flags, effective UID and private
namespace. Never select internal Mac storage or the current worker/database pendrive implicitly.
No such target is currently authorized/provisioned. The current noowners pendrive is ineligible.

Future operator procedure, requiring a separate bounded authorization before execution:

1. Founder names an existing eligible external volume and an expendable synthetic-only test
   subtree, evidence location, permitted fault classes and cleanup owner. If no such volume
   exists, stop; do not purchase, format, remount, encrypt or change ownership under this task.
   Target must not contain worker databases/credentials or share physical power-loss risk
   with them. An identifier placeholder cannot authorize a path or device.
2. Pin paths from `/` one component at a time with directory/no-follow/CLOEXEC opens; reject
   `..` and links. Permit only the recorded external mount transition. Retain each parent;
   check fstat + no-follow stat of each child from its parent, native mount facts and volume
   attributes. Trust root-owned system anchors only after verifying ordinary users cannot
   replace children: conservatively reject group/other write and nonempty extended ACLs.
   Apply the same nonreplaceability checks to the volume root/intermediate directories,
   allowing owner root or effective UID. In the selected private evidence tree require
   owner=effective UID, exact 0700
   directories/0600 regular files and empty extended ACLs. Reject regular files with nlink !=1.
   If conservative ancestor rules reject the host, record ineligibility; do not repair it.
3. Record a read-only eligibility result before authorizing writes. Free space proposed for
   later bounded tests: at least 3x total synthetic input bytes +100 MiB, rechecked before
   creation; this does not reserve blocks or remove ENOSPC risk. Runtime must check support
   on every run, not trust a prior diskutil printout or a mount pathname.
4. Later, separately authorize empty creation and ordinary-account denial tests, before
   evidence writes. Verify probe and each empty output via fd (owner/mode/ACL/mount); a
   permissive umask must not broaden explicit modes. Another ordinary account must fail
   traversal/read and namespace replacement; writer os.access is not this test. No account
   setup or account operation is part of B0a or the next metadata-only experiment.
5. Durability eligibility additionally requires the publication/flush matrix on that exact
   filesystem/device. Unsupported directory sync/full flush is a rejection, not an ignored
   EINVAL or substitution with F_BARRIERFSYNC. Physical tests require their own explicit
   device-specific approval; simulated EIO and process kill cannot qualify power-loss behavior.

## Candidate lifecycle and on-disk states

Every step is proposed, blocked by the verdicts above. Fresh generation name is one Store-
validated component. All children are fixed Store names; imported paths cannot select them.
Revalidate pinned fstat/entry, mount and private-access facts before/after each read/write
and publication step. This is sampled detection; **C1/C2 still apply**.

| Step | Operation and retained state | Observable state / durable claim |
| --- | --- | --- |
| P0 | Start monotonic 60s budget before Store.prepare. Pin/validate target and inputs. | N: no new generation; no evidence output. |
| P1 | mkdirat via `os.mkdir(dir_fd=parent)` mode 0700, exclusively; open generation fd and exclusive empty `.privacy.probe`, verify privacy; unlink only that verified empty probe via generation fd; exclusive-open fixed outputs 0600 with O_NOFOLLOW/O_CLOEXEC. | E: private empty objects only. A mkdir success/open failure leaves an untrusted empty entry to quarantine, not reopen. |
| P2 | Read/hash only pinned inputs; write complete report bytes with bounded short-write loops, validating each empty output before its first evidence byte. | W: partial/full reports, no public marker. Surfaced Python I/O errors or zero-progress writes abort; Store adds no error retry. Raw EINTR may be retried inside Python before Store regains control (interruption layers above). |
| P3 | Flush language buffers; fsync + F_FULLFSYNC both report fds; fsync + F_FULLFSYNC generation and parent fds. | F: reports and generation naming have *requested* ordered persistence; all calls must return success. Directory behavior untested. |
| P4 | Exclusive-create `.completion.pending`, verify empty privacy, write exact contract marker using byte hashes, fsync + F_FULLFSYNC marker fd; flush generation fd again. | T: prepared marker, still no completion.json. Temporary name is never a reader completion signal. |
| P5 | Check budget/identities/privacy; bridge exclusive rename of pending marker. | V: completion.json visible; a complete hash pair may exist, but rename alone is not durable acknowledgement. |
| P6 | fsync + F_FULLFSYNC generation then parent; recheck all identities/privacy and budget; close owned handles, capturing failures. | D: flushes/checks returned; no stdout yet. V/D may survive a subsequent error or kill (C3). |
| P7 | Emit exactly the existing SDD success summary/exit 0/1/3 only if all preceding returns were successful before expiry. | A: external observer received summary. Check-to-summary gap, blocked stdout and scheduling remain G4/G8 blockers. |

No native call is a transaction over P0–P7. On returning failure stop new work, emit fixed
Diagnostic/exit 4, close owned fds, and preserve the generation; no error-path overwrite,
unlink-to-hide or fallback. After loss, do not touch paths until an operator verifies identity
for a **new** attempt. Recovery opens freshly verified storage under a separate run, checks
regular/private files and both exact hashes. N/E/W/F/T or invalid V => incomplete/quarantine;
valid V/D/A => integrity-recoverable, acknowledgement unknown absent an external observer.
This distinction exposes the SDD fatal-marker conflict rather than declaring it resolved.
No data is claimed durable solely from a syscall request, process-kill survival or valid hash.

## Finite fault matrix (all unperformed)

Setup common to F-01–24: proposed target, synthetic canary bytes only, known input/output
hashes, clean generation name, independent observer, and sentinel inventories of any allowed
replacement trees. **S** = deterministic injected return/schedule in a future test double;
**K** = real process termination on authorized scratch storage; **H** = physical device loss
or power interruption under separate authorization. S cannot prove native enforcement; K
does not discard drive caches; H observations cover only the recorded device/model/trials.
Future kernel/account tests require explicit authorization even when listed alongside S.
For S variants, Python I/O doubles inject surfaced exceptions/return counts at Store's
call boundary; bridge doubles inject ABI status/errno, or explicitly identified native
stubs test the bridge's mapping/no-retry rule. Neither proves actual syscall interruption.
A mocked `InterruptedError` tests Store's surfaced-error path only, not Python's handling
of raw EINTR, signal-handler timing or safe cancellation. Record the injection layer in E0.

Common evidence **E0** for every row: source/bridge SHA and artifact hash, runtime/OS/SDK/device
profile, test ID and concrete variant, before/after input hashes, monotonic operation/fault/
ack trace, fd identities and numeric returns, stdout/stderr/exit or signal, post-recovery
file/marker bytes and hashes, and unchanged replacement-tree sentinels. Record read failure
as unknown, never as absence. No private evidence or absolute operator paths enter public logs.
“Old state” means pre-existing objects are unchanged. F-xx variants listed within a row form
the finite expansion; P-position ranges name each position, not random sampling.

| ID / class | Injection point and input/setup | Expected visible / durable state | Caller oracle; recovery disposition | Evidence beyond E0 |
| --- | --- | --- | --- | --- |
| F-01 / S, later native control | Eligible target, tiny complete canary reports, no fault, P0–P7. | N→E→W→F→T→V→D→A; exact marker/hash pair. Persistence remains unverified until H. | Existing summary and 0/1/3 only after P6; recover exact generation. | Ordered flush and identity-check returns; choose pass/fail/unknown in three variants. |
| F-02 / S | P0: noowners, non-APFS, read-only, wrong owner, missing UUID, missing ACL capability-valid bit, missing rename-exclusive capability-valid bit (7 variants). | N; old state unchanged, zero evidence writes. | E_IO/4, no summary; reject target. | Failed predicate and zero write-call count. |
| F-03 / S, later account test | P1: umask 000, inherited allow-read ACE, inherited allow-delete ACE (3 variants). | umask control E with 0700/0600 then A if all succeeds; either ACE => at most E, no evidence. | Control succeeds only with denial test; ACL variants E_IO/4; quarantine empty generation. | Empty-object mode/ACL returns; separately authorized foreign open/traverse/replacement denial. |
| F-04 / S | Replace pinned volume-root path after P0; substitute a directory on another volume. | No replacement writes; original at most E/W before detection; absent marker required. | E_IO/4 on sampled mismatch, no summary; verify original volume before retry. | Root-entry versus retained-root tuple and replacement sentinels. |
| F-05 / S | Swap one ancestor after P0, during P2 read, between P2 output writes, immediately before P5 (4 variants). | Original partial state only; no substituted-tree output; no marker before P5. | R7 requires E_IO/4/no summary in all variants; quarantine originals. | Independent fault times; parent/child tuple at next checkpoint. |
| F-06 / S | Replace input leaf during P2 read; replace output leaf between P2 writes (2 variants). | Retained fd accesses original leaf; replacement untouched; mismatch abort, no valid marker. | E_IO/4; original input unchanged; explicit new attempt only. | fd/name dev+inode mismatch; read-byte hash and both leaf sentinels. |
| F-07 / S | Swap and restore ancestor entirely between two P2 identity checks. | Candidate may reach valid A on original tree; no redirected writes. | **Required R7 oracle: no success. Candidate can fail oracle** (C2); quarantine test outcome, keep NO-GO. | Fault-driver trace despite equal sampled tuples; never label a successful run a passing R7 test. |
| F-08 / S | Mount fsid mismatch, UUID mismatch, flags mismatch or I/O loss at P2 read, P2 write, pre-P5, post-P5/pre-P6 (16 variants). | Pre-P5: partial original, no marker; post-P5: V possible; actual persistence unknown until original target is accessible. | E_IO/4 if call returns, no summary/no fallback; V requires hash inspection, not assumed absence. | Each native return and retained tuple; post-P5 conflict with fatal-marker wording recorded. |
| F-09 / S | P0 input/private-parent nonempty ACL, P1 wrong output owner, P4 broad inherited marker ACL (3 variants). | N for P0; at most empty output for P1; F/T with empty rejected marker at P4. No byte enters rejected object. | E_IO/4; preserve/quarantine originals; no permissions repair. | Write count for rejected descriptor =0; saved owner/empty-ACL facts. |
| F-10 / S, later controlled account test | Persistent drift after P2 check; drift/read/restore within one P2 gap (2 variants). | Persistent drift detected only later; transient drift may expose canary and still reach A. | R5 requires no exposure/no success; **candidate fails universal oracle** (C1). Stop; do not pass on eventual rejection alone. | Ordinary-account read outcome and ACL event intervals; synthetic only. |
| F-11 / S | P1 pre-existing generation; competing creator at mkdir; existing report leaf before its exclusive open (3 variants). | Old bytes/inodes unchanged; at most empty new directory in leaf variant; no truncation/marker. | E_IO/4; preserve colliding object, no automatic name retry. | Old/new inode+hash inventory, EEXIST return. |
| F-12 / S, later native | P5 pre-existing completion.json; competing creator immediately before rename (2 variants). | Existing marker untouched; T remains; no overwrite. | COLLISION→E_IO/4/no summary; quarantine this attempt, do not interpret hostile/pre-existing marker as its success. | Exclusive-rename capability and EEXIST; both marker hashes. |
| F-13 / S | Python-call boundary: P2 short-write count then completion; zero count; surfaced OSError(ENOSPC) after a prefix of report.json, report.html, or P4 marker; surfaced InterruptedError at P2 read or write (7 variants). | Short-write control may reach A; other variants W/T partial, never new completion.json. | Control loops only over remaining bytes within budget; surfaced errors/zero write => E_IO/4 and quarantine, no Store retry. | Byte offsets/counts; zero-progress termination; original hashes unchanged. InterruptedError doubles do not exercise raw EINTR or implicit interpreter retries. |
| F-14 / S | P3/P4 fsync or F_FULLFSYNC fails on each of two reports or temporary marker (6 variants). | W/F/T; no public marker; persisted bytes indeterminate. | E_IO/4, no summary; quarantine until verified cleanup. | Exact failing fd/stage/errno; absence of P5 call. |
| F-15 / S | P3 generation/parent or P4 generation directory sync/full-flush fails (6 variants). | W/F/T; no public marker, naming persistence unknown. | E_IO/4; reject unsupported target on EINVAL/ENOTSUP; no weaker flush fallback. | Per-directory operation and error, no P5. |
| F-16 / S | Native rename stub inside bridge returns -1 with EIO, ENOTSUP or EINTR (3 variants). | T or V must be inspected; do not assert rollback on ambiguous failure. | Bridge SYSTEM_ERROR, UNSUPPORTED, SYSTEM_ERROR respectively => E_IO/4, no summary; quarantine/inspect original target. | Stub invocation count =1; no bridge or Store retry. Simulated errno mapping is not proof of actual native interruption or effects. |
| F-17 / S | P6 generation/parent fsync/full-flush fails (4 variants). | V may persist intact; no claim of acknowledged durability. | E_IO/4/no summary; valid pair is recoverable but cannot meet absolute “no complete marker” (C3). | Visible marker and reported failure together. |
| F-18 / K | Kill at E, mid-W, F, mid-P4, T (5 variants). | Absent or partial generation, never a new valid completion.json; cached bytes may survive. | Signal termination/no summary; quarantine incomplete output. | Observer kill/exit timestamps; recovery with caches still potentially live. |
| F-19 / K | Kill after P5 before P6; after P6 before P7 (2 variants). | V/D may survive with both hashes; marker cannot prove acknowledgement. | No summary; recover integrity only, not prior caller success. | Independent acknowledgement observer and marker inspection (C3). |
| F-20 / S | Surface Python OSError at each acquisition stage (anchor, ancestor, input, generation, output, marker) or close; inject bridge SYSTEM_ERROR at mount, volume or ACL query (10 variants). | State never advances beyond failure; no writes through closed/reused fd; possible partial originals. | E_IO/4 (or E_INTERNAL for lifetime defect), no summary; retain partial state. | Open/close ledger balances owned handles on these surfaced-error paths; bridge never closes borrowed fd; no blind close retry. Does not establish safety under asynchronous handler exceptions. |
| F-21 / H | Explicitly approved physical detach/power interruption at P2, pre-P5, post-P5/pre-P6, post-P6/pre-P7, after observed A (5 variants). | N/W/T/V/D may be absent, partial or intact until inspected; after A require exact pair on recoverable supported device. Total device loss is outside disk-loss guarantee. | R7 requires no success for pre-A loss; final-check gap may violate it (C2). After A, record recovery/durability failure separately. | Device-specific trigger time, power/controller details, post-reconnect verified original identity; no worker drive permitted. |
| F-22 / S, later separately bounded kernel-block test | S holds the Store-visible call boundary for open, read, write, metadata query, full-flush, rename, close, or stdout beyond 60s (8 variants); include operation issued just before deadline. | Early block: N/W at most; rename/late block: V/D possible even after caller times out. | Required E_LIMIT/4 by deadline, no complete marker/no late work; **not established by signals/watchdog** (C4); record violations, no pass by timer firing alone. | Monotonic start/deadline/return/termination and any late I/O; descriptor liveness until actually released. S does not validate kernel blocking or interpreter EINTR retries; future native observations must distinguish syscall attempts from return to Store. |
| F-23 / S | Recovery: absent marker, truncated marker, bad JSON hash, bad HTML hash, valid pair without observed acknowledgement (5 variants). | First four incomplete; fifth integrity-recoverable, acknowledgement unknown. | Reject incomplete; do not fabricate original success or overwrite any generation. | Reader's independent byte hashes and exact disposition. |
| F-24 / S, later metadata probe | ABI mismatch; short/malformed volume payload; packed UUID with absent returned bit; ACL NULL; valid empty ACL; nonempty ACL; ACL unexpected entry error; acl_free failure (8 variants). | N; no mutation by metadata-only bridge calls. | Invalid/unsupported fails E_IO/4; empty/nonempty classified without confusing Darwin 0 with end-of-list. | Allocation/free ledger, output payload unusable on failure, retained caller fd usable after call. |

Matrix variants are bounded test proposals, not a license to execute them. For unavailable
fault controls or unobservable disk states, record **unverified**, not pass. Destructive
tests on a volume shared with source/history are explicitly ineligible.

## Smallest next experiment and remaining gates

Recommend exactly one separately scoped experiment **E1: read-only native metadata ABI probe**,
only after founder/coordinator authorization names T-EXT-APFS-1 and permits compiling a
scratch harness. Use a pre-existing authorized empty private directory plus pre-existing
empty-ACL/nonempty-ACL canary objects supplied by the operator. Build only the three metadata
exports and version query; query mount/ACL once per canary fd and volume attributes once on
the retained volume-root fd, plus F-24's finite simulated return cases. Open existing fds
read-only, record masks/ACL classification and allocation/fd balance,
then close. No marker publication export, output writes, account tests, package install or
database access. Keep build/log artifacts in an explicitly approved pendrive location.
The operator must authorize that location; this document chooses no new path or device.

E1 answers ABI/layout and metadata compatibility, **not** G1 effective denial, G4 continuous
identity, G7 durability or G8 deadline. Stop on unsupported/malformed data, target mismatch,
missing authorization or blocked call; report unknown rather than adding fallback behavior.
External observation of a hung probe is required; no hard kill-time promise follows from E1.
No target is available now, so E1 is **not currently authorized or runnable**. Founder decisions
D1–D4 remain necessary before a publication experiment can claim to meet requirements.

Unresolved beyond storage: CPython 3.14.10/rfc8785 0.1.4 compatibility and JCS conformance,
strict numeric-token policy, exact pip/build/backend locks, native build/link/distribution
provenance and license inventory, supported OS/libc/SDK binding, resource measurements and
independent expectation review. B1/M0 stay blocked; AI stays beyond deterministic/pilot gates.
Approving this documentation does not approve E1 or another task.

## Primary sources and inspected declarations

Retrieved/inspected **2026-11-19**. Sources describe semantics, not a successful capability
test. Apple's archived manuals predate APFS. Public source revisions below were identified
from the upstream main commit during retrieval; neither is claimed to match the installed
kernel/libc binary. Review source license obligations before copying implementation code;
this document copies none. SDK declarations were read, not linked or executed.

| ID | Primary evidence | Claim and limitation |
| --- | --- | --- |
| S1 | Python 3.14.10 [os.open](https://docs.python.org/release/3.14.10/library/os.html#os.open), [os.read](https://docs.python.org/release/3.14.10/library/os.html#os.read), [os.write](https://docs.python.org/release/3.14.10/library/os.html#os.write); [Apple open](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/open.2.html) | Descriptor-relative operations (B0 research); O_CREAT/O_EXCL/no-follow and mode/umask semantics. Each cited Python function documents implicit EINTR retry if the handler does not raise. No continuous namespace lock, foreign-access proof or bounded return to Store. |
| S2 | [Apple fstatfs](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fstatfs.2.html) | Facts about an open fd's filesystem; ownership-ignore flags. Not an unrepeatable mount epoch or loss event log. |
| S3 | [Apple XNU getattrlist manual](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/bsd/man/man2/getattrlist.2) | fgetattrlist fd semantics, four-byte payload alignment/order, full-size/invalid packing, returned vs supported/native attribute masks, capability-valid bits, UUID and exclusive-rename support. Source revision, not installed behavior. |
| S4 | [Apple ACL retrieval](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/acl_get_fd.3.html) | Independent ACL copy, NULL/error and acl_free ownership. Copy does not participate in enforcement. |
| S5 | [Apple ACL iteration manual](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/acl_get_entry.3.html), [Libc acl_entry.c](https://github.com/apple-oss-distributions/Libc/blob/71bbe350ab79eef58113991d817ccc6165061a64/posix1e/acl_entry.c), [acl.c](https://github.com/apple-oss-distributions/Libc/blob/71bbe350ab79eef58113991d817ccc6165061a64/posix1e/acl.c) | Entry success=0; validated FIRST_ENTRY on empty list gives EINVAL in source. acl_valid is not proof of effective access. Target libc conformance remains E1's question. |
| S6 | [Apple fsync](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fsync.2.html), [fcntl](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fcntl.2.html) | fsync alone does not guarantee drive-cache persistence; F_FULLFSYNC requests it and may take a long time; devices can ignore requests. No APFS directory-flush proof or 60-second bound. |
| S7 | [Apple XNU rename manual](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/bsd/man/man2/rename.2) | renameatx_np relative directory fds, RENAME_EXCL/EEXIST, ENOTSUP; ordinary rename overwrites. Namespace operation is not acknowledgement/durability transaction. |
| S8 | Python 3.14.10 signal: [handler execution](https://docs.python.org/release/3.14.10/library/signal.html#execution-of-python-signal-handlers), [handlers and exceptions](https://docs.python.org/release/3.14.10/library/signal.html#note-on-signal-handlers-and-exceptions) | Handler execution can be deferred while C runs; raised exceptions may arrive after any bytecode instruction and leave unexpected state. Neither signal delivery nor raising proves bounded cancellation or safe descriptor lifetime/cleanup. Even a process watchdog lacks a reviewed end-to-end bound here. |
| S9 | Installed Apple SDK 27.2 at `xcrun --show-sdk-path`, targeted headers below | Current declarations corroborate API availability at compile time only. No native capability execution. |

S9 inspected paths relative to SDK root: `usr/include/sys/mount.h` (fstatfs line 442,
MNT_IGNORE_OWNERSHIP 229); `sys/attr.h` under the same include root (options 48–50,
capability/attribute types 125/404, no-permissions/volume-group masks 290/292,
rename-exclusive capability 397, returned mask 456, volume masks 502–512);
`sys/acl.h` (acl_free 152, acl_get_entry/acl_valid 160/161, acl_get_fd_np 197);
`sys/stdio.h` (RENAME_EXCL 37, renameatx_np 53); `sys/fcntl.h` (no-follow/directory/CLOEXEC
123/141/153, F_FULLFSYNC 260, openat 621); `unistd.h` (fsync 623, fgetattrlist 761/769);
`sys/stat.h` (fstatat/mkdirat 393/394). Some declarations are conditional: C ABI must use
the compiled SDK types, never transcribe archived structs into Python.

Documentation verification and actual CI outcomes belong to the issue-linked delivery PR.
No F-* case, E1, privacy test, benchmark, write probe, native compile, unplug or power-loss
experiment has run. Three broad SDK-manpage glob searches were denied by the harness;
public Apple manuals/source supplied semantics without retrying that directory search.
