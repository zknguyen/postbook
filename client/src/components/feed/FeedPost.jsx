import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
// import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

import { useAuth } from '../../contexts/AuthContext';
import { likePost, unlikePost } from '../../redux/state/postsSlice.jsx';
import CommentForm from '../posts/CommentForm.jsx';

// GraphQL mutations
const LIKE_FEED_POST = gql`
  mutation likeFeedPost($postId: ID!, $userId: ID!) {
    likePost(postId: $postId, userId: $userId) {
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

const UNLIKE_FEED_POST = gql`
  mutation unlikeFeedPost($postId: ID!, $userId: ID!) {
    unlikePost(postId: $postId, userId: $userId) {
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

const FeedPost = ({ feedPost }) => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [likeFeedPost] = useMutation(LIKE_FEED_POST);
  const [unlikeFeedPost] = useMutation(UNLIKE_FEED_POST);

  const hasLiked = feedPost.post.likes.some((like) => like.userId === user.UserID);

  // Local state for comment input
  const [showCommentInput, setShowCommentInput] = useState(false);

  const handleUserClick = () => {
    navigate(`/user/${feedPost.user.userId}`);
  };

  const handlePostClick = () => {
    navigate(`/post/${feedPost.post.postId}`);
  };

  const handleLike = async () => {
    try {
      const response = await likeFeedPost({
        variables: { postId: feedPost.post.postId, userId: user.UserID }
      });
      dispatch(likePost(response.data));
    } catch (error) {
      console.error('Could not like post: ', error);
    }
  };

  const handleUnlike = async () => {
    try {
      const response = await unlikeFeedPost({
        variables: { postId: feedPost.post.postId, userId: user.UserID }
      });
      dispatch(unlikePost(response.data));
    } catch (error) {
      console.error('Could not unlike post: ', error);
    }
  };

  const handleCommentButtonClick = () => {
    setShowCommentInput((prev) => !prev);
  };

  return (
    <div className="bg-neutral-800 text-left rounded-lg justify-start w-100% m-1 p-2">
      <p className="font-bold m-2 hover:underline hover:cursor-pointer" onClick={handleUserClick}>{feedPost.user.username}</p>
      <p className="m-2">{feedPost.post.textContent}</p>
      {feedPost.post.mediaUrl && <img src={feedPost.post.mediaUrl} alt="Post media" className="w-full h-auto rounded-lg" />}
      <p className="text-neutral-400 !text-sm m-2">{feedPost.post.numLikes}</p>
      <hr className="border-neutral-400 m-2" />
      <div className="flex justify-between items-center m-2">
        {hasLiked ? (
          <button
            className="!text-xs !bg-neutral-800 h-6 hover:!bg-neutral-700 hover:!border-none"
            onClick={handleUnlike}
          >
            Unlike
          </button>
        ) : (
          <button
            className="!text-xs !bg-neutral-800 h-6 hover:!bg-neutral-700 hover:!border-none"
            onClick={handleLike}
          >
            Like
          </button>
        )}
        <button
          className="!text-neutral-400 !text-xs !bg-neutral-800 h-6 hover:!bg-neutral-700 hover:!border-none"
          onClick={handleCommentButtonClick}
        >
          Comment
        </button>
        <button
          className="!text-neutral-400 !text-xs !bg-neutral-800 h-6 hover:!bg-neutral-700 hover:!border-none"
          onClick={handlePostClick}
        >
          Share
        </button>
      </div>
      {showCommentInput && <CommentForm postId={feedPost.post.postId} userId={user.UserID} />}
    </div>
  );
};

export default FeedPost;