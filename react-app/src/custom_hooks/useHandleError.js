import RedirectToLink from "../supporting_hooks/RedirectToLink";

const useHandleError = (error) => {
    if (error !== null) {
        if (error === 'Internal Server Error') {
            alert('Something went wrong. Please try again later.');
        }
        else {
            let errorMessage = JSON.parse(error)['error'];
            if (errorMessage === 'Investments not linked.') {
                RedirectToLink('investments');
            }
            else if (errorMessage === 'Transactions Not Linked.') {
                RedirectToLink('transactions'); 
            }
        }
    }
}

export default useHandleError;