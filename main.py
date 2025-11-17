from psched.database import create_database, create_post_entry, return_next_post_entry
from psched.post import Post

def main():
    print("Hello from postschedule!")
    create_database()

    p = Post.create("Taitol", "Contentchi")
    print(repr(p))

    create_post_entry(p)
    print(repr(p))

    nextposts = return_next_post_entry()
    print(repr(nextposts))
    
    

if __name__ == "__main__":
    main()
