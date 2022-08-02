import React, {useContext} from 'react';
import AuthContext from "../context/AuthContext";

const HomePage = () => {
    let {user} = useContext(AuthContext)
    return (
        <div>
            {user && <p>Hello {user.email}, you are logged to the HOME page!</p>}
        </div>
    );
}

export default HomePage;