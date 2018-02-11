"""Automatically close a PR as it opens."""

import gidgethub.routing
router = gidgethub.routing.Router()


@router.register("pull_request", action="opened")
@router.register("pull_request", action="reopened")
async def close_pr(event, gh, *args, **kwargs):
    close_the_pr(event, gh)


def close_the_pr(event, gh):
    data = {'state': 'closed',
            'maintainer_can_modify': True}
    gh.patch(event.data["pull_request"]["url"], data=data)
    pr_comment = {
        'body': "Close it. I'm a bot."
    }

    print("getitem")
    print(pr_comment)

    for item in gh.getiter('/repos/mariatta/cpython/git/refs/heads'):
        print(item)

    gh.post(event.data["pull_request"]["comments_url"], data=pr_comment)