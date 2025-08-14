import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useAuth } from "../../contexts/AuthContext";
import { setPosts } from '../../redux/state/postsSlice.jsx';
import { gql, useQuery } from '@apollo/client';
import FeedPost from './FeedPost.jsx';

const GET_FEED_POSTS = gql`
  query getFeedPosts($userId: ID!) {
    feedPosts(userId: $userId) {
      feedPostId
      user {
        userId
        username
      }
      post {
        postId
        textContent
        numLikes
        mediaUrl
        likes {
          userId
        }
      }
    }
  }
`;

const Feed = () => {
  const { user } = useAuth();

  const postsState = useSelector((state) => state.posts);
  const dispatch = useDispatch();

  const { loading, data, refetch } = useQuery(GET_FEED_POSTS, {
    variables: { userId: user.UserID },
  });

  const { posts, newPost, modifiedPost } = postsState;


  useEffect(() => {
    const fetchFeedPosts = async () => {
      if (user != null && user.hasOwnProperty('UserID')) {
        try {
          if (!loading && data) {
            await refetch({ userId: user.UserID });
            dispatch(setPosts(data.feedPosts));
          }
        } catch (error) {
            console.error('Error fetching posts:', error);
        }
      }
    };

    if (user) {
      fetchFeedPosts();
    };
  }, [user, newPost, modifiedPost, data, refetch]);

  return (
    <>
      <div className="my-5">
      {posts.map(feedPost => (
        <FeedPost feedPost={feedPost} key={feedPost.feedPostId} />
      ))}
      </div>
    </>
  )
}

export default Feed;