
```go
def get_user_by_username(db: Session, username: str):
    # case-sensitive
    # only work for MySQL
    # return db.query(User).filter(func.binary(User.username) == username).first()
    # work for SQLite
    # return db.query(User).filter(User.username.collate("binary") == username).first()
    
    # Determine the dialect being used
    dialect = db.bind.dialect.name
    
    # Different queries for MySQL and SQLite
    if dialect == 'mysql':
        sql = text(
            """
            SELECT * FROM users
            WHERE BINARY username = :username
            LIMIT 1
            """
        )
    elif dialect == 'sqlite':
        sql = text(
            """
            SELECT * FROM users
            WHERE username COLLATE BINARY = :username
            LIMIT 1
            """
        )
    else:
        raise NotImplementedError(f"Database dialect '{dialect}' is not supported.")

    """
    With raw SQL query,
    db.execute(sql).fetchone() returned a raw result row from the database (ResultProxy object - a lower-level result set),
    not a mapped User object.
    When you tried to access model-specific attributes like following or other SQLAlchemy-managed features (e.g., relationships, _sa_instance_state),
    it threw an error because these attributes don't exist in the raw row.
    """
    result = db.execute(sql, {'username': username}).mappings().fetchone()

    # If result is found, map the result dictionary to a User object
    if result:
        user = User(
            id=result['id'],
            username=result['username'],
            email=result['email'],
            password=result['password'],
            bio=result['bio'],
            image=result['image']
        )
        return user

    return None

    # SQLAlchemy provides a convenient way to use raw SQL but still return ORM-mapped objects via the .from_statement() method.
    result = db.query(User).from_statement(sql).params(username=username).first()
    return result

    # dialect = db.bind.dialect.name
    # if dialect == 'mysql':
    #     return db.query(User).filter(func.binary(User.username) == username).first()
    # elif dialect == 'sqlite':
    #     return db.query(User).filter(User.username.collate("binary") == username).first()
    # else:
    #     raise NotImplementedError(f"Database dialect '{dialect}' is not supported.")
```

The error you're seeing when querying the user by username using raw SQL and then trying to append the user to current_user.following likely stems from the dual usage of raw SQL queries and SQLAlchemy ORM within the same transaction.

When you use a raw SQL query to retrieve the user and then interact with SQLAlchemy's ORM, the objects returned by the raw SQL query are not fully recognized by SQLAlchemy's session or ORM. This can lead to conflicts, including duplicate entry errors or inconsistencies with session management.

Here's why this happens and how to resolve it:

Why the Error Occurs:
Raw SQL bypasses the SQLAlchemy ORM session: When you query a user via a raw SQL statement (e.g., text()), the returned result is not tracked by the SQLAlchemy ORM session. It is simply a dictionary or a raw database result, and SQLAlchemy doesn't know that it corresponds to an existing model in its session.

ORM expects session-bound objects: SQLAlchemy ORM manages the identity of objects within the session. When you retrieve a User instance via the ORM (db.query(User)), the ORM knows this object and manages its state. When you use raw SQL, the returned result is not bound to the session, so when you try to append it to a relationship or commit it, the ORM sees it as a new, untracked object, leading to IntegrityError due to primary key constraints.

Resolution:
You should avoid mixing raw SQL queries and ORM in the same flow. If you want to query a user and manage relationships, it’s best to stick to SQLAlchemy ORM.

Fix:
Instead of querying the user with raw SQL, use the ORM to ensure that the object is properly managed by the session.

Here’s how you can modify the get_user_by_username function to use ORM properly:

python
Copy code
def get_user_by_username(db, username):
    """
    Retrieve a user by username using SQLAlchemy ORM.
    """
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            print(f"No user found with username: {username}")
            return None
        return user
    except Exception as e:
        print(f"Error retrieving user by username: {e}")
        return None
And in your follow_user function, ensure you’re always using ORM-managed objects:

python
Copy code
def follow_user(db: Session, current_user: User, user_to_follow: User) -> User:
    """
    Follow a user, ensuring that the current user isn't already following the target user.
    """
    # Load the current user with the 'following' relationship
    current_user = db.query(User).options(joinedload(User.following)).filter_by(id=current_user.id).first()

    if not current_user:
        raise ValueError("Current user not found")

    # Ensure user_to_follow is a valid User instance and exists using ORM
    user_to_follow = db.query(User).filter_by(id=user_to_follow.id).first()
    if not user_to_follow:
        raise ValueError("User to follow does not exist")

    # Check if the user_to_follow is already in the current_user's following list
    if user_to_follow in current_user.following:
        return user_to_follow

    # Add the existing user_to_follow to the current_user's following list
    current_user.following.append(user_to_follow)

    # Commit transaction
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("An error occurred while trying to follow the user. This may be due to a primary key violation or other database constraints.") from e

    return user_to_follow
Key Points:
Avoid raw SQL for ORM-managed objects: Use SQLAlchemy ORM to fetch and manage objects when you're working with relationships or session-bound operations.
Use the ORM session to track object state: This ensures that SQLAlchemy knows which objects are already in the session and avoids primary key conflicts.
By following these guidelines, you should avoid the IntegrityError and ensure smooth handling of user data in your follow_user function.