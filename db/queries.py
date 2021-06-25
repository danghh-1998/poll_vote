class Q:
    GET_ALL__POLL = """
        SELECT * FROM polls
    """

    INSERT__POLL = """
        INSERT INTO polls (id, title, creator_id, type, allow_add_choice, allow_multiple_choice, created_at, 
            updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    UPDATE__POLL = """
        UPDATE polls set title = %s, allow_add_choice = %s, allow_multiple_choice = %s, updated_at = %s
        WHERE id = %s
    """

    DELETE__POLL = """
        DELETE FROM polls WHERE id = %s
    """

    GET_BY_ID__POLL = """
        SELECT DISTINCT 
            polls.*,
            votes.id,
            votes.title,
            votes.image,
            votes.creator_id,
            votes.last_user_update,
            votes.count,
            GROUP_CONCAT(DISTINCT user_votes.user_id ORDER BY user_votes.user_id ASC separator ',') AS user_votes
        FROM votes
                 INNER JOIN polls on votes.poll_id = polls.id
                 LEFT JOIN user_votes ON votes.id = user_votes.vote_id
        WHERE poll_id = %s
        GROUP BY votes.id, votes.title, votes.image, votes.creator_id, votes.last_user_update, votes.count 
    """

    COUNT_USER_VOTES__POLL = """
        SELECT COUNT(*)
        FROM polls
        INNER JOIN votes ON polls.id = votes.poll_id
        INNER JOIN user_votes ON votes.id = user_votes.vote_id
        WHERE polls.id = %s
    """

    GET_IDS_BY_POLL_ID__VOTE = """
        SELECT id
        FROM votes
        WHERE poll_id = %s
    """

    INSERT__VOTE = """
        INSERT INTO votes (id, title, image, creator_id, last_user_update, poll_id, count, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    GET_ALL_BY_POLL_ID__VOTE = """
        SELECT id, title, image, creator_id, last_user_update, count, 
            GROUP_CONCAT(DISTINCT user_votes.user_id ORDER BY user_votes.user_id ASC separator ',') AS user_votes
        FROM votes LEFT JOIN user_votes ON votes.id = user_votes.vote_id
        WHERE poll_id = %s
        GROUP BY id, title, creator_id, last_user_update, count
    """

    GET_BY_POLL_ID__VOTE = """
        SELECT id, title, image, creator_id, last_user_update, count
        FROM votes
        WHERE poll_id = %s AND id = %s
    """

    UPDATE__VOTE = """
        UPDATE votes SET title = %s, image = %s, last_user_update = %s, updated_at = %s
        WHERE id = %s
    """

    DELETE__VOTE = """
        DELETE FROM votes
        WHERE id = %s
    """

    COUNT_USER_VOTES__VOTE = """
        SELECT COUNT(*)
        FROM votes INNER JOIN user_votes on votes.id = user_votes.vote_id
        WHERE vote_id = %s
    """

    GET_MYSELF__VOTE = """
        SELECT id FROM user_votes INNER JOIN votes ON user_votes.vote_id = votes.id WHERE user_id = %s AND poll_id = %s
    """

    INCREASE_COUNT__VOTE = """
        UPDATE votes SET count = count + 1 WHERE id = %s
    """

    DECREASE_COUNT__VOTE = """
        UPDATE votes SET count = count - 1 WHERE id = %s
    """

    GET_BY_VOTE_ID__USER_VOTE = """
        SELECT user_id FROM user_votes WHERE vote_id = %s
        ORDER BY created_at
    """

    PAGING = """
        LIMIT %s
        OFFSET %s
    """

    INSERT__USER_VOTE = """
        INSERT INTO user_votes (vote_id, user_id, created_at) 
        VALUES (%s, %s, %s)
    """

    DELETE__USER_VOTE = """
        DELETE FROM user_votes WHERE user_id = %s AND vote_id = %s 
    """

    COUNT_BY_VOTE_ID__USER_VOTE = """
        SELECT COUNT(*) AS total FROM votes INNER JOIN user_votes ON votes.id = user_votes.vote_id WHERE votes.id = %s 
    """
