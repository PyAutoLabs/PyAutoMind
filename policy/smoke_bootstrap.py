# Generated from PyAutoMind/policy/smoke_bootstrap.py; edit the source, not copies.
# CI supplies build_util on PYTHONPATH. Discovery is only a local fallback.
try:
    import build_util
except ModuleNotFoundError as _smoke_import_error:
    if _smoke_import_error.name != "build_util":
        raise  # An installed Hands dependency is broken, not missing Hands.

    def _smoke_hands_path():
        import importlib.util

        explicit = os.environ.get("PYAUTO_ROOT")
        if explicit:
            root = Path(explicit).expanduser().resolve()
        else:
            root = next(
                (p for p in WORKSPACE.parents if (p / ".pyauto-root").is_file()),
                WORKSPACE.parent,
            )
            # Prefer the shared resolver, but never require Brain. A bundle's
            # Brain may be a symlink to canonical; reject that foreign answer.
            resolvers = [p for p in (
                root / "PyAutoBrain" / "agents" / "_pyauto_root.py",
                root / "organs" / "PyAutoBrain" / "agents" / "_pyauto_root.py",
            ) if p.is_file()]
            if len({p.resolve() for p in resolvers}) > 1:
                raise RuntimeError("PyAutoBrain has distinct flat and grouped checkouts")
            resolver_file = resolvers[0] if resolvers else None
            if resolver_file is not None:
                try:
                    spec = importlib.util.spec_from_file_location(
                        "_smoke_root_resolver", resolver_file
                    )
                    resolver = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(resolver)
                    resolved = Path(resolver.workspace_root_reason()[0]).resolve()
                    if resolved in WORKSPACE.parents:
                        root = resolved
                except (Exception, SystemExit):
                    pass  # Missing/broken optional resolver cannot break discovery.
        flat = root / "PyAutoHands" / "autohands"
        grouped = root / "organs" / "PyAutoHands" / "autohands"
        if (flat / "build_util.py").is_file() and (grouped / "build_util.py").is_file() and flat.resolve() != grouped.resolve():
            raise RuntimeError("PyAutoHands has distinct flat and grouped checkouts")
        hands = grouped if (grouped / "build_util.py").is_file() else flat
        if not (hands / "build_util.py").is_file():
            raise ModuleNotFoundError(
                f"PyAutoHands not found for {WORKSPACE}; looked for "
                f"{hands / 'build_util.py'}. Supply PyAutoHands/autohands on "
                "PYTHONPATH or set PYAUTO_ROOT to the intended workspace root.",
                name="build_util",
            )
        return hands

    sys.path.insert(0, str(_smoke_hands_path()))
    import build_util

AUTOHANDS = Path(build_util.__file__).resolve().parent
