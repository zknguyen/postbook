import { useEffect } from 'react';
import { useParams } from "react-router-dom";
import { gql, useQuery } from '@apollo/client';

const GET_POSTS = gql`
  query {
    posts(userId: 2) {
      userId
      postId
      textContent
      comments {
        userId
        textContent
      }
    }
  }
`;

const UserProfile = () => {
  const { userId } = useParams();

  const { loading, data, refetch } = useQuery(GET_POSTS, {
      variables: { userId: userId },
      fetchPolicy: "network-only",
    });
  
  // TODO: Move this formatting to a main page component
  return (
    <div className="grid grid-cols-3 w-full justify-self-center text-left my-4">
      <div
        className="
          col-start-2
        "
      >
        <h1>User Profile: {userId}</h1>
        {loading && <p>Loading...</p>}
        {data && (
          <ul>
            {data.posts.map(post => (
              <div
                key={post.postId}
                className="
                  bg-neutral-800 text-left
                  rounded-lg justify-start
                  w-100%
                  m-1 p-2
                "
              >
                <h2>Post: {post.postId}</h2>
                <h2>{post.textContent}</h2>
                <hr className="border-neutral-400 m-2" />
                <ul>
                  {post.comments.map(comment => (
                    <li key={comment.userId}>{comment.textContent}</li>
                  ))}
                </ul>
              </div>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default UserProfile;

