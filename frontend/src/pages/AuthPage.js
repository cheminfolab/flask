import React, {useContext, useState, useEffect} from 'react';
import AuthContext from "../context/AuthContext";

export default function AuthPage() {

  let {loginUser, registerUser} = useContext(AuthContext)
  let [authMode, setAuthMode] = useState("login")
  let [groups, setGroups] = useState([])

  useEffect(() => {
      getGroups();
  }, [])

  let getApiResponse = async (items, setState) => {
    let response = await fetch('http://127.0.0.1:8000/api/'+String(items), {
        method:'GET',
        headers:{
            'Content-Type':'application/json',
        }
    })
    let data = await response.json()
    if(response.status === 200){
        setState(data)
    }else if(response.statusText === 'Unauthorized'){
        console.log("An error occurred.")
    }
  }

  let getGroups = () => getApiResponse('group/', setGroups)


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
            <label>Working Group</label>
            <select className="form-select form-select-sm mt-1" name="working_group" aria-label=".form-select-sm example">
            {/* todo: add working group request */}
              <option selected>select group</option>
              {groups.map(({id, name}) => (
                <option key={id} value={id}>{name}</option>
              ))}
              {/*<option value="2">Brasholz</option>*/}
              {/*<option value="3">Fifelsky</option>*/}
            </select>
          </div>
          <div className="form-group mt-3">
            <label>Status</label>
            <select className="form-select form-select-sm mt-1" name="status" aria-label=".form-select-sm example">
              <option selected>select status</option>
              <option value="1">student</option>
              <option value="2">phd</option>
              <option value="3">staff</option>
            </select>
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