import './SubstanceImage.css'
import {Image} from "react-bootstrap";

const SubstanceImage = ({path, className=null, onClick=null}) => (
    <Image
        src={process.env.REACT_APP_API_BASE_URL+String(path)}
        alt={'chemical structure'}
        className={className}
        onClick={onClick}
        rounded
    />
)
export default SubstanceImage;