import React, {useContext} from 'react';
import AuthContext from "../context/AuthContext";

const ReactionPage = () => {
    let {user} = useContext(AuthContext)
    return (
        <div>
            {user && <p>Hello {user.username}, you are logged to the REACTION page!</p>}
        </div>
    );
}

export default ReactionPage;