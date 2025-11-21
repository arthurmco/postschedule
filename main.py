from psched.database import create_database_if_not_exist, create_post_entry, return_next_post_entry
from psched.post import Post
import argparse

import os

def open_editor_in_file_and_retrieve_content(filepath, *, delete_if_exists=True):
    editor = os.getenv("EDITOR")
    if editor is None:
        editor = "vim"

    if delete_if_exists:
        if os.path.exists(filepath):
            os.remove(filepath)

    os.system(f"{editor} {filepath}")

    with open(filepath, "r") as f:
        return f.read()


def cmd_create_post(args):
    ctnt = open_editor_in_file_and_retrieve_content("content.txt")
    p = Post.create(args.title, ctnt)
    create_post_entry(p)    

def cmd_list_post(args):
    nextposts = return_next_post_entry(30)
    if len(nextposts) == 0:
        print("No next posts")
    
    for p in nextposts:
        print(f"{p.title} {p.content[:30]}...")

    print("")

def cmd_pull_post(args):
    nextposts = return_next_post_entry()
    if len(nextposts) == 0:
        print("No next posts. Create a post, please")
    
    curpost = nextposts[0]
    print("Copying to clipboard not yet implemented...")
    print("")
    print(f"TITLE: {curpost.title}")
    print(f"{curpost.content}")
    
    
def main():
    parser = argparse.ArgumentParser(
        prog='postschedule',
        description='Schedule and pull social network posts')

    subparsers = parser.add_subparsers(help="subcommands", required=True)
    p_create = subparsers.add_parser("create", help="Create a post")
    p_create.add_argument("title", help="Post title (might not appear in the post)", type=str)
    p_create.set_defaults(func=cmd_create_post)
    
    p_list = subparsers.add_parser("list", help="List post entries")
    p_list.set_defaults(func=cmd_list_post)
    
    p_pull = subparsers.add_parser("pull",
                                   help="Pull a post into the clipboard to be pasted on the site")
    p_pull.set_defaults(func=cmd_pull_post)
    
    p_post = subparsers.add_parser("post", help="Register a pulled post (the most recent pull by default)")
    p_delete = subparsers.add_parser("delete", help="Delete a post")    

    
    args = parser.parse_args()    

    create_database_if_not_exist()
    args.func(args)


if __name__ == "__main__":
    main()
