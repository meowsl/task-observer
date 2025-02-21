export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface User {
  firstname: string
  username: string
}

export interface UserRegistration {
  username: string
  firstname: string
  password: string
  password_confirm: string
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
}