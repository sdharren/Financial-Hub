import {Link} from 'react-router-dom';

export default function Header({
    heading,
    paragraph,
    linkName,
    linkUrl="#"
}){
    return(
        <div className="mb-10">
            <h2 className="mt-6 text-center text-3xl font-extrabold text-white-900">
                {heading}
            </h2>
            <p className="mt-2 text-center text-sm text-white-600 mt-5">
            {paragraph} {' '}
            <Link to={linkUrl} className="font-medium text-orange-600 hover:text-purple-500">
                {linkName}
            </Link>
            </p>
        </div>
    )
}