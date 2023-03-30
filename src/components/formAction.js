/**
 * The form action button for the login/register button on the login and signup
 * page.
 */

export default function FormAction({
    handleSubmit,
    type = 'Button',
    action = 'submit',
    text
}) {
    return (
        <div>
        {
            type === 'Button' ?
            <button
                type = {action}
                className = "flex justify-center w-full py-2 border border-transparent text-sm font-medium rounded-md text-white bg-orange-600 hover:bg-hover-color focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 mt-10"
                onSubmit = {handleSubmit}
            >
                {text}
            </button>:
            <div></div>
        }
        </div>
    )
}