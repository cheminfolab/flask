import React, {useContext, useState} from 'react';
import AuthContext from "../context/AuthContext";

export default function AuthPage() {

  let {loginUser, registerUser} = useContext(AuthContext)

  let [authMode, setAuthMode] = useState("login")

  const changeAuthMode = () => {
    setAuthMode(authMode === "login" ? "register" : "login")
  }

  if (authMode === "login") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={loginUser}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Log In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Register
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Username</label>
              <input
                name="username"
                type="text"
                className="form-control mt-1"
                placeholder="Enter username"
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                name="password"
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
              Forgot <a href="#">password?</a>
            </p>
          </div>
        </form>
      </div>
    )
  }

  return (
    <div className="Auth-form-container">
      <form className="Auth-form"onSubmit={registerUser}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Register</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>
              Log In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>First Name</label>
            <input
              name="first_name"
              type="text"
              className="form-control mt-1"
              placeholder="First Name"
            />
          </div>
          <div className="form-group mt-3">
            <label>Last Name</label>
            <input
              name="last_name"
              type="text"
              className="form-control mt-1"
              placeholder="Last Name"
            />
          </div>
          <div className="form-group mt-3">
            <label>Username</label>
            <input
              name="username"
              type="text"
              className="form-control mt-1"
              placeholder="Username"
            />
          </div>
          <div className="form-group mt-3">
            <label>Working Group</label>
            <input
              name="working_group"
              type="text"
              className="form-control mt-1"
              placeholder="Working Group"
            />
          </div>
          <div className="form-group mt-3">
            <label>Status</label>
            <input
              name="status"
              type="text"
              className="form-control mt-1"
              placeholder="e.g. student"
            />
          </div>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              name="email"
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
            />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              name="password"
              type="password"
              className="form-control mt-1"
              placeholder="Password"
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
          <p className="text-center mt-2">
            Forgot <a href="#">password?</a>
          </p>
        </div>
      </form>
    </div>
  )
}

// export default AuthPage;