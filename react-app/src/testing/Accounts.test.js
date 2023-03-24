// import React from 'react';
// import { render, fireEvent } from '@testing-library/react';
// import Accounts from '../pages/Accounts';
// import { BrowserRouter } from 'react-router-dom';
// import { AuthProvider } from '../context/AuthContext';

// describe('Accounts', () => {
//   // Define some sample data to use for testing
//   const banks = ['Bank A', 'Bank B'];
//   const brokerages = ['Brokerage A', 'Brokerage B'];

//   it('renders the component with the correct headings', () => {
//     const { getByText } = render( 
//       <BrowserRouter>
//         <AuthProvider>
//             <Accounts />
//         </AuthProvider>
//       </BrowserRouter>);
//     expect(getByText('Accounts')).toBeInTheDocument();
//     expect(getByText('Name')).toBeInTheDocument();
//     expect(getByText('Type')).toBeInTheDocument();
//     expect(getByText('Remove')).toBeInTheDocument();
//   });

//   it('renders a table row for each bank in the list', () => {
//     const { getByText } = render( 
//     <BrowserRouter>
//         <AuthProvider>
//             <Accounts banks={banks}/>
//         </AuthProvider>
//       </BrowserRouter>);
//     banks.forEach((bank) => {
//       expect(getByText(bank)).toBeInTheDocument();
//       expect(getByText('Institution')).toBeInTheDocument();
//       expect(getByText('Remove')).toBeInTheDocument();
//     });
//   });

//   it('renders a table row for each brokerage in the list', () => {
//     const { getByText } = render(
//     <BrowserRouter>
//         <AuthProvider>
//             <Accounts brokerages={brokerages}/>
//         </AuthProvider>
//       </BrowserRouter>);
//     brokerages.forEach((brokerage) => {
//       expect(getByText(brokerage)).toBeInTheDocument();
//       expect(getByText('Brokerage')).toBeInTheDocument();
//       expect(getByText('Remove')).toBeInTheDocument();
//     });
//   });

//   it('removes a bank from the list when the remove button is clicked', () => {
//     const { getByText, queryByText } = render(
//        <BrowserRouter>
//         <AuthProvider>
//             <Accounts banks={banks} handleRemoveBank={() => {}} />
//         </AuthProvider>
//       </BrowserRouter>
      
//     );
//     const bankToRemove = banks[0];
//     fireEvent.click(getByText(`Remove`, { selector: 'button' }));
//     expect(queryByText(bankToRemove)).not.toBeInTheDocument();
//   });

//   it('removes a brokerage from the list when the remove button is clicked', () => {
//     const { getByText, queryByText } = render(
//         <BrowserRouter>
//         <AuthProvider>
//             <Accounts brokerages={brokerages} handleRemoveBrokerage={() => {}} />
//         </AuthProvider>
//       </BrowserRouter>
//     );
//     const brokerageToRemove = brokerages[0];
//     fireEvent.click(getByText(`Remove`, { selector: 'button' }));
//     expect(queryByText(brokerageToRemove)).not.toBeInTheDocument();
//   });
// });

