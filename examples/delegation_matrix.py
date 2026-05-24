"""Print delegation routes for sample phrases."""

from multi_agent.delegation import DelegationRouter

SAMPLES = [
    "research papers on transformers",
    "refactor the auth module",
    "write a blog post",
    "review this design for risks",
    "analyze the sales csv",
    "plan the migration milestones",
]


def main() -> None:
    router = DelegationRouter()
    for phrase in SAMPLES:
        role = router.route(phrase)
        print(f"{phrase!r} -> {role.value}")


if __name__ == "__main__":
    main()
