import {useContext} from 'react';
import AuthContext from "../context/AuthContext";
import {AuthContextType} from "../@types/authorization";

const HomePage = () => {
    let {user} = useContext(AuthContext) as AuthContextType
    return (
        <div>
            {user && <p>Hello {user.email}, you are logged to the HOME page!</p>}
        </div>
    );
}

export default HomePage;