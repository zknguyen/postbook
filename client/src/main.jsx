import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import store from './redux/store.jsx'
import { AuthProvider } from './contexts/AuthContext.jsx'
import './index.css'
import App from './App.jsx'
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';

const apolloClient = new ApolloClient({
  uri: import.meta.env.VITE_APOLLO_CLIENT_URI,
  cache: new InMemoryCache(),
  headers: {
    // Add any necessary headers here
  },
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'no-cache',
    }
  },
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <ApolloProvider client={apolloClient}>
        <AuthProvider>
          <Provider store={store}>
            <App />
          </Provider>
        </AuthProvider>
      </ApolloProvider>
    </BrowserRouter>
  </StrictMode>,
)
