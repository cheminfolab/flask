import React from 'react';
import './SubstanceImage.css'

const SubstanceImage = ({path}) => {
    return (
        <div>
            <img src={'http://127.0.0.1:8000'+String(path)} alt={'chemical structure'}/>
        </div>
    );
}

export default SubstanceImage;