import {useContext, useState, useEffect} from 'react';
import AuthContext from "../context/AuthContext";
import {Button, Col, Form, Row} from "react-bootstrap";
import {AuthContextType, AuthModeType, Errors, RegistrationForm} from "../@types/authorization";
import {Group} from "../@types/accounts";

export default function AuthPage() {

  let {loginUser, registerUser} = useContext(AuthContext) as AuthContextType
  let [authMode, setAuthMode] = useState<AuthModeType>("login")
  let [groups, setGroups] = useState<Group[] | []>([])

  // todo: use axios
  let getApiResponse = async (items, setState) => {
    let response = await fetch('http://127.0.0.1:8000/api/'+String(items), {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    let data = await response.json()
    if (response.status === 200){
        setState(data)
    } else if (response.statusText === 'Unauthorized'){
        console.log("An error occurred.")
    }
  }

  let getGroups = () => getApiResponse('group/', setGroups);

  useEffect(() => {
      getGroups();
  }, [])

  const changeAuthMode = () => {setAuthMode(authMode === "login" ? "register" : "login")}

  // VALIDATION

  const [form, setForm] = useState<RegistrationForm>({
    "first_name": null,
    "last_name": null,
    "working_group": null,
    "status": null,
    "email": null,
    "password": null,
    "password2": null
  })
  const [errors, setErrors] = useState<Errors>({})

  const setField = (field, value) => {
    setForm({
      ...form,
      [field]:value,
    })

    if (!!errors[field])
      setErrors({
          ...errors,
        [field]:null,
      })
  }

  const validateForm:() => Errors = () => {
    const newErrors: Errors = {
      "first_name": null,
      "last_name": null,
      "working_group": null,
      "status": null,
      "email": null,
      "password": null,
      "password2": null
    }
    const NAME_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{2,23}/i
    const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,120}$/i
    const validName = name => NAME_REGEX.test(name)
    const validPassword = pwd => PWD_REGEX.test(pwd)

    // todo: LOGIN
    // https://www.youtube.com/watch?v=86uXSFm3ND0

    // REGISTRATION
    if (!form.first_name || form.first_name === '') newErrors.first_name = 'Please enter your first name.'
    else if (!validName(form.first_name))
      newErrors.first_name = 'Please enter a valid name. It must have 2 to 24 characters and begin with a letter. Letters, numbers, underscores, hyphens allowed.'
    if (!form.last_name || form.last_name === '') newErrors.last_name = 'Please enter your last name.'
    else if (!validName(form.last_name))
      newErrors.last_name = 'Please enter a valid name. It must have 2 to 24 characters and begin with a letter. Letters, numbers, underscores, hyphens allowed.'
    if (!form.working_group) newErrors.working_group = 'Please select a working group.'
    // validation
    if (!form.status) newErrors.status = 'Please select your status.'
    // validation
    if (!form.email || form.email === '') newErrors.email = 'Please enter an email address.'
    // email validation
    if (!form.password || form.password === '') newErrors.password = 'Please enter a password.'
    else if (!validPassword(form.password))
      newErrors.password = 'Please enter a valid password. It must have 8 to 120 characters and include uppercase and lowercase letters, a number and a special character. Allowed characters are: !@#¢%'
    if (!form.password2 || form.password2 === '') newErrors.password2 = 'Please confirm your password.'
    else if (form.password2 !== form.password)
      newErrors.password2 = 'Password entered does not match the first password'
    return newErrors
  }

  const handleSubmit = event => {
    event.preventDefault()
    const formErrors = validateForm()
    if (Object.keys(formErrors).length > 0) setErrors(formErrors)
    else if (authMode === 'login') loginUser(event)
    else registerUser(event)
  }



  if (authMode === "login") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={loginUser}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Log In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>Register</span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                autoFocus
                required
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
                required
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
              Forgot <a href="/#">password?</a>
            </p>
          </div>
        </form>
      </div>
    )
  }

  return (
    <div className="Auth-form-container">
      <Form className="Auth-form" noValidate //validated={validated}
            onSubmit={handleSubmit}
      >
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Register</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>Log In</span>
          </div>

          <Row className="mt-3">
            <Form.Group as={Col} md="5" controlId="first_name">
              <Form.Label>First name</Form.Label>
              <Form.Control
                required
                name="first_name"
                type="text"
                placeholder="First name"
                value={form.first_name}
                onChange={ event => setField('first_name', event.target.value)}
                isInvalid={!!errors.first_name}
              />
              <Form.Control.Feedback type="invalid">{errors.first_name}</Form.Control.Feedback>
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
            <Form.Group as={Col} md="7" controlId="last_name">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                required
                name="last_name"
                type="text"
                placeholder="Last Name"
                value={form.last_name}
                onChange={ event => setField('last_name', event.target.value)}
                isInvalid={!!errors.last_name}
              />
              <Form.Control.Feedback type="invalid">{errors.last_name}</Form.Control.Feedback>
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
          </Row>
          <Row className="mt-3">
            <Form.Group as={Col} md="6" controlId="working_group">
              <Form.Label>Working Group</Form.Label>
              <Form.Select
                  required
                  name="working_group"
                  value={form.working_group}
                  onChange={ event => setField('working_group', event.target.value)}
                  isInvalid={!!errors.working_group}
                  >
                <option>select...</option>
                {groups.map(({id, name}) => <option key={id} value={id}>{name}</option>)}
              </Form.Select>
              <Form.Control.Feedback type="invalid">{errors.working_group}</Form.Control.Feedback>
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
            <Form.Group as={Col} md="6" controlId="status">
              <Form.Label>Status</Form.Label>
              <Form.Select
                  required
                  name="status"
                  value={form.status}
                  onChange={ event => setField('status', event.target.value)}
                  isInvalid={!!errors.status}
              >
                <option>select...</option>
                <option value="1">student</option>
                <option value="2">phd</option>
                <option value="3">staff</option>
              </Form.Select>
              <Form.Control.Feedback type="invalid">{errors.status}</Form.Control.Feedback>
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
          </Row>
          <Form.Group className="mb-3 mt-3" controlId="email">
            <Form.Label>Email Address</Form.Label>
            <Form.Control
              required
              name="email"
              type="email"
              placeholder="Email Address"
              value={form.email}
              onChange={ event => setField('email', event.target.value)}
              isInvalid={!!errors.email}
            />
            <Form.Control.Feedback type="invalid">{errors.email}</Form.Control.Feedback>
            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3 mt-3" controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control
                required
                name="password"
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={ event => setField('password', event.target.value)}
                isInvalid={!!errors.password}
            />
            <Form.Control.Feedback type="invalid">{errors.password}</Form.Control.Feedback>
            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3 mt-3" controlId="password2">
            <Form.Label>Password Confirmation</Form.Label>
            <Form.Control
                required
                name="password2"
                type="password"
                placeholder="Password"
                value={form.password2}
                onChange={ event => setField('password2', event.target.value)}
                isInvalid={!!errors.password2}
            />
            <Form.Control.Feedback type="invalid">{errors.password2}</Form.Control.Feedback>
            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
          </Form.Group>

          <Button type="submit" className="mt-3">Submit</Button>

          <p className="text-center mt-2">
            Forgot <a href="/#">password?</a>
          </p>
        </div>
      </Form>
    </div>
  )
}