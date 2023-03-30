/**
 * Header component that goes above each form component for the login page and
 * the sign up page.
 */
import {Link} from 'react-router-dom';

export default function Header({
    heading,
    paragraph,
    linkName,
    linkUrl="#"
}){
    return(
        <div className="mb-10 mt-5">
            <h2 className="text-center text-3xl font-bold text-white">
                {heading}
            </h2>
            <p className="text-center text-white mt-5">
            {paragraph} {' '}
            <Link to={linkUrl} className="font-medium text-orange-600 hover:text-hover-color">
                {linkName}
            </Link>
            </p>
        </div>
    )
}