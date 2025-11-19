import { Link } from "react-router"
import { useContext, type ComponentProps} from "react"
import { cn } from "@/lib/utils"
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
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import AuthContext from "@/contexts/AuthContext"
import type { AuthContextType } from "../types/authorization"

const LoginForm = ({className, ...props}: ComponentProps<"div">) => {

    const {loginUser} = useContext(AuthContext) as AuthContextType

    return(
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
            <CardHeader>
                <CardTitle>Login to your account</CardTitle>
                <CardDescription>
                Enter your email below to login to your account
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={loginUser}>
                    <FieldGroup>
                        <Field>
                        <FieldLabel htmlFor="email">Email</FieldLabel>
                        <Input
                            id="email"
                            type="email"
                            placeholder="m@example.com"
                            required
                        />
                        </Field>
                        <Field>
                        <div className="flex items-center">
                            <FieldLabel htmlFor="password">Password</FieldLabel>
                            <Link
                                to="#"
                                className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                            >
                            Forgot your password?
                            </Link>
                        </div>
                        <Input id="password" type="password" required />
                        </Field>
                        <Field>
                        <Button type="submit">Login</Button>
                        <FieldDescription className="text-center">
                            Don&apos;t have an account? <Link to="/signup">Sign up</Link>
                        </FieldDescription>
                        </Field>
                    </FieldGroup>
                </form>
            </CardContent>
            </Card>
        </div>
    )    
}

export default LoginForm
