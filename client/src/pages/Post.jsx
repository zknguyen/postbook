import { useParams } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { gql, useQuery, useMutation } from '@apollo/client';

const GET_POST = gql`
  query getPost($postId: ID!) {
    post(postId: $postId) {
      userId
      textContent
      comments {
        userId
        commentId
        textContent
      }
    }
  }
`;

const COMMENT_FEED_POST = gql`
  mutation addComment($postId: ID!, $userId: ID!, $textContent: String!) {
    addComment(postId: $postId, userId: $userId, textContent: $textContent) {
      textContent
    }
  }
`;

const Post = () => {
  const { postId } = useParams();

  const postState = useSelector((state) => state.posts);
  const dispatch = useDispatch();

  const [addComment] = useMutation(COMMENT_FEED_POST);

  const { loading, data, refetch } = useQuery(GET_POST, {
    variables: { postId: postId },
    fetchPolicy: "network-only",
  });

  const { post } = postState;

  const handleUserClick = () => {
    Console.WriteLine()
    // navigate(`/user/${feedPost.user.userId}`);
  };

  const handleComment = async () => {
    try {
      const commentText = prompt('Enter your comment:');
      if (commentText) {
        console.log('Adding comment:', commentText);
        const response = await addComment({
          variables: {
            postId: feedPost.post.postId,
            userId: user.UserID,
            textContent: commentText,
          }
        });
        // Handle the response if needed, e.g., update UI or state
        console.log('Comment added:', response.data);
      }
    } catch (error) {
      console.error('Could not comment on post: ', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!data || !data.post) return <div>No post found.</div>;

  // TODO: Move this formatting to a main page component
  return (
    <div className="grid grid-cols-3 w-full justify-self-center text-left my-4">
      <div
        className="
          col-start-2
          bg-neutral-800 rounded-lg p-2 my-5
        "
      >
        <h3>User: {data.post.userId}</h3>
        <h3>{data.post.textContent}</h3>
        <hr className="border-neutral-400 m-2" />
        {data.post.comments.map(comment => (
          <div key={comment.commentId} className="bg-neutral-700 rounded-lg p-2 my-3">
            <p className="text-sm" onClick={handleUserClick}>User: {comment.userId}</p>
            <p className="text-sm">{comment.textContent}</p>
          </div>
        ))}
        <form>
          <input
            type="text"
            className="
              text-[#D3D3D3] bg-neutral-700
              rounded-lg border-none
              w-full
              px-2 py-1
              my-1
              focus:outline-none
            "
            placeholder="Add a comment..."
          />
        </form>
      </div>
    </div>
  )
}

export default Post;