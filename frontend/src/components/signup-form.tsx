import {
    useContext,
    useEffect, 
    useState, 
    type ComponentProps, 
    type FormEventHandler 
} from "react"
import { Link } from "react-router"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import type { Group } from "@/types/accounts"
import AuthContext from "@/contexts/AuthContext"
import type { 
    AuthContextType, 
    Errors, 
    FormValidator, 
    RegistrationForm 
} from "@/types/authorization"
import useAxios from "@/hooks/useAxios"
import { 
    Select, 
    SelectContent, 
    SelectGroup, 
    SelectItem, 
    SelectLabel, 
    SelectTrigger, 
    SelectValue 
} from "./ui/select"

const SignupForm = ({ ...props }: ComponentProps<typeof Card>) => {

    const {registerUser} = useContext(AuthContext) as AuthContextType
    const [groups, setGroups] = useState<Group[]>([])
    const emptyForm = {
        first_name: undefined,
        last_name: undefined,
        working_group: undefined,
        status: undefined,
        email: undefined,
        password: undefined,
        password_confirm: undefined
    }
    const [errors, setErrors] = useState<Errors>(emptyForm)
    const [form, setForm] = useState<RegistrationForm>(emptyForm)
    const [submitted, setSubmitted] = useState<boolean>(false)

    const api = useAxios()

    useEffect(() => {
        api
            .getAll("/group/")
            .then(groups => setGroups(groups))
            .catch() // TODO: alert!
    }, [])

    const setField = (field: keyof RegistrationForm, value: number | string) => {
        setForm({...form, [field]: value})
    }

    const validateForm: FormValidator = () => {
        const NAME_REGEX = /^[a-zA-Z][a-zA-Z]{1,23}$/
        const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{7,119}$/
        const validName = (name: string) => NAME_REGEX.test(name)
        const validPassword = (pwd: string) => PWD_REGEX.test(pwd)
        // TODO: validate email
        
        const newErrors: Errors = emptyForm
        
        // first name
        if (!form.first_name || form.first_name === "") newErrors.first_name = "Please enter your first name."
        else if (!validName(form.first_name)) {
            newErrors.first_name = "Please enter a valid name. It must have 2 to 24 characters and begin with a letter. Special characters are not allowed."            
        }
        // last name
        if (!form.last_name || form.last_name === "") newErrors.last_name = "Please enter your last name."
        else if (!validName(form.last_name)) {
            newErrors.last_name = "Please enter a valid name. It must have 2 to 24 characters and begin with a letter. Special characters are not allowed."
        }
        // working group
        if (!form.working_group) newErrors.working_group = "Please select a working group."
        // role
        if (!form.status) newErrors.status = "Please select your status."
        // email
        if (!form.email || form.email === "") newErrors.email = "Please enter an email address."
        // password
        if (!form.password || form.password === "") newErrors.password = "Please enter a password."
        else if (!validPassword(form.password)) {
            newErrors.password = "Please enter a valid password. It must have 8 to 120 characters and include uppercase and lowercase letters, a number and a special character. Allowed characters are: !@#¢%"
        }
        if (!form.password_confirm || form.password_confirm === "") newErrors.password_confirm = "Please confirm your password."
        else if (form.password_confirm !== form.password) {
            newErrors.password_confirm = "Password entered does not match the first password"
        }

        return newErrors
    }

    const handleSubmit: FormEventHandler<HTMLFormElement> = event => {
        event.preventDefault()
        const formErrors = validateForm()
        if (Object.keys(formErrors).length > 0) {
            setErrors(formErrors)
        }
        else registerUser(event)
        setSubmitted(true)
        // TODO: handle already registered user
    }

    const FieldFeedback = ({name}: {name: keyof RegistrationForm}) => {
        if (submitted){
            if (!!errors[name]) return <FieldError>{errors[name]}</FieldError>
            else if (!!form[name]) return <FieldDescription>Looks good!</FieldDescription>
        }
    }

    return(
        <Card {...props}>
            <CardHeader>
                <CardTitle>Create an account</CardTitle>
                <CardDescription>
                    Enter your information below to create your account
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit}>
                    <FieldGroup>
                        <div className="grid grid-cols-2 gap-4">
                            <Field data-invalid={!!errors.first_name}>
                                <FieldLabel htmlFor="first_name">First Name</FieldLabel>
                                <Input 
                                    id="first_name" 
                                    type="text" 
                                    placeholder="John"
                                    onChange={event => setField("first_name", event.target.value)}
                                    aria-invalid={!!errors.first_name}
                                    // required
                                />
                                <FieldFeedback name="first_name" />
                            </Field>
                            <Field data-invalid={!!errors.last_name}>
                                <FieldLabel htmlFor="last_name">Last Name</FieldLabel>
                                <Input 
                                    id="last_name" 
                                    type="text" 
                                    placeholder="Doe"
                                    onChange={event => setField("last_name", event.target.value)}
                                    aria-invalid={!!errors.last_name}
                                    // required  
                                />
                                <FieldFeedback name="last_name" />
                            </Field>
                        </div>
                        <div className="grid grid-cols-3 gap-4">
                            <Field 
                                data-invalid={!!errors.working_group}
                                className="col-span-2"
                            >
                                <FieldLabel htmlFor="working_group">Group</FieldLabel>
                                <Select
                                    aria-invalid={!!errors.working_group}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select a working group" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectGroup>
                                            <SelectLabel>Ruhr-Universität Bochum</SelectLabel>
                                            {groups.map(group => (
                                                <SelectItem
                                                    key={group.id}
                                                    value={group.id.toString()}
                                                >
                                                    {group.name}
                                                </SelectItem>
                                            ))}
                                        </SelectGroup>
                                    </SelectContent>
                                </Select>
                                {/* <Input 
                                    id="working_group" 
                                    type="text" 
                                    placeholder="John"
                                    onChange={event => setField("working_group", event.target.value)}
                                    aria-invalid={!!errors.working_group}
                                    // required
                                /> */}
                                <FieldFeedback name="working_group" />
                            </Field>
                            <Field
                                data-invalid={!!errors.status}
                                className="col-span-1"
                            >
                                <FieldLabel htmlFor="status">Role</FieldLabel>
                                <Input 
                                    id="status" 
                                    type="text"
                                    placeholder="PhD"
                                    onChange={event => setField("status", event.target.value)}
                                    aria-invalid={!!errors.status}
                                    // required  
                                />
                                <FieldFeedback name="status" />
                            </Field>
                        </div>
                        <Field>
                            <FieldLabel htmlFor="email">Email</FieldLabel>
                            <Input
                                id="email"
                                type="email"
                                placeholder="m@example.com"
                                onChange={event => setField("email", event.target.value)}
                                aria-invalid={!!errors.email}
                                // required
                            />
                            <FieldDescription>
                                We&apos;ll use this to contact you. We will not share your email
                                with anyone else.
                            </FieldDescription>
                            <FieldFeedback name="email" />
                        </Field>
                        <Field>
                            <FieldLabel htmlFor="password">Password</FieldLabel>
                            <Input 
                                id="password" 
                                type="password" 
                                onChange={event => setField("password", event.target.value)}
                                aria-invalid={!!errors.password}
                                // required 
                            />
                            <FieldFeedback name="password" />
                        </Field>
                        <Field>
                            <FieldLabel htmlFor="password_confirm">
                                Confirm Password
                            </FieldLabel>
                            <Input 
                                id="password_confirm" 
                                type="password" 
                                onChange={event => setField("password_confirm", event.target.value)}
                                aria-invalid={!!errors.password_confirm}
                                // required
                            />
                            <FieldFeedback name="password_confirm" />
                        </Field>
                        <FieldGroup>
                            <Field>
                            <Button type="submit">Create Account</Button>
                            <FieldDescription className="px-6 text-center">
                                Already have an account? <Link to="/login">Log in</Link>
                            </FieldDescription>
                            </Field>
                        </FieldGroup>
                    </FieldGroup>
                </form>
            </CardContent>
        </Card>
    )
}

export default SignupForm