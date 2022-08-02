import React, {useContext} from 'react';
import AuthContext from "../context/AuthContext";

const ProjectPage = () => {
    let {user} = useContext(AuthContext)
    return (
        <div>
            {user && <p>Hello {user.email}, you are logged to the PROJECTS page!</p>}
        </div>
    );
}

export default ProjectPage;