/**
 * Creates the <Input /> component from the given object, expected to be a form
 * field object.
 */

const fixedInputClass="rounded-md bg-input-field-purple relative block w-full px-3 py-2 border border-input-field-purple  text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm"

export default function Input({
    handleChange,
    labelText,
    labelFor,
    id,
    name,
    type,
    isRequired=false,
    placeholder,
    customClass
}){
    return(
        <div className="my-5">
            <label htmlFor={labelFor} className="sr-only">
              {labelText}
            </label>
            <input
              onChange={handleChange}
              id={id}
              name={name}
              type={type}
              required={isRequired}
              className={fixedInputClass+customClass}
              placeholder={placeholder}
            />
          </div>
    )
}
