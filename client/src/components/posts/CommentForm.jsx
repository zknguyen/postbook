import { useState, useRef } from 'react';
import { gql, useMutation } from '@apollo/client';

const COMMENT_FEED_POST = gql`
  mutation addComment($postId: ID!, $userId: ID!, $textContent: String!) {
    addComment(postId: $postId, userId: $userId, textContent: $textContent) {
      textContent
    }
  }
`;

const CommentForm = ({ postId, userId }) => {
  const [commentText, setCommentText] = useState('');

  const [addComment] = useMutation(COMMENT_FEED_POST);


  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    try {
      if (commentText.trim()) {
        await addComment({
          variables: {
            postId: postId,
            userId: userId,
            textContent: commentText,
          }
        });
        setCommentText('');
      }
    } catch (error) {
      console.error('Could not comment on post: ', error);
    }
  };

  return (
    <form onSubmit={handleCommentSubmit} className="flex flex-col gap-2 mt-2 animate-fade-in">
      <div className="flex">
        <input
          className="
            bg-neutral-700 text-[#D3D3D3]
            rounded-l-lg border-none
            px-2 py-1
            focus:outline-none
          "
          type="text"
          value={commentText}
          onChange={e => setCommentText(e.target.value)}
          placeholder="Write a comment..."
          autoFocus
          required
        />
      </div>
      <div className="flex gap-2">
        <button type="submit" className="bg-blue-600 text-white rounded px-3 py-1 text-xs">Post</button>
      </div>
    </form>
  )
};

export default CommentForm;