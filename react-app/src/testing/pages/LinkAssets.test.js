// import React from 'react';
// import { render, screen } from '@testing-library/react';
// import LinkAssets from '../../pages/LinkAssets';
// import { BrowserRouter, MemoryRouter } from 'react-router-dom';
// import { AuthProvider } from '../../context/AuthContext';
// import App from '../../App';

// describe('LinkAssets component', () => {
//     const user = { name: 'Test User', email: 'test@example.com' };
//     const PrivateRouteWrapper = ({ children }) => (
//       <AuthProvider value={{ user }}>
//         {children}
//       </AuthProvider>
//     );

//   it('renders without crashing', () => {
//     render(
//         <MemoryRouter initialEntries={[LinkAssets]}>
//           <PrivateRouteWrapper>
//             <App />
//           </PrivateRouteWrapper>
//         </MemoryRouter>
//     );
//     const linkassets = screen.queryByTestId('linkassetstest');
//     expect(linkassets).toBeDefined();
//   });

//   it('contains the "home_page" class', () => {
//     const { container } = render(
//         <MemoryRouter initialEntries={['/link_assets']}>
//           <PrivateRouteWrapper>
//             <App />
//           </PrivateRouteWrapper>
//         </MemoryRouter>
//       );
//       expect(container.querySelector('.asset__content')).toBeInTheDocument();
//   });

//   it('contains the "home_boxes" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider value={{ user }}>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.background__image')).toBeInTheDocument();
//   });

//   it('contains the "home_text_holder" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.middle-text')).toBeInTheDocument();
//   });

//   it('contains the "home__content__holder" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.link-button')).toBeInTheDocument();
//   });

//   it('contains the "home__box" class', () => {render(
//     <BrowserRouter>
//     <AuthProvider>
//     <LinkAssets />
//     </AuthProvider>
//     </BrowserRouter>);
//     expect(container.querySelector('.assetLink_holder')).toBeInTheDocument();
//   });

//   it('contains the "home__background_image" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.debit__card__image')).toBeInTheDocument();
//   });

//   it('contains the "home__content" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.background__box')).toBeInTheDocument();
//   });

//   it('contains the "home-text" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.bank__image')).toBeInTheDocument();
//   });

//   it('contains the "home__first__image" class', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.crypto__image')).toBeInTheDocument();
//   });

//   it('has the correct source for the "home__background__image" element', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.debit__card__image').src).toEqual('http://localhost/asset-debit.png');
//   });

//   it('has the correct source for the "home__background__image" element', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.bank__image').src).toEqual('http://localhost/asset-bank.png');
//   });

//   it('has the correct source for the "home__background__image" element', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.crypto__image').src).toEqual('http://localhost/asset-crypto.png');
//   });

//   it('has the correct alt text for the "home__background__image" element', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.debit__card__image').alt).toEqual('#');
//   });

//   it('has the correct alt text for the "home__first__image" elements', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelectorAll('.bank__image').alt).toEqual('#');
    
//   });

//   it('has the correct alt text for the "home__background__image" element', () => {
//     const { container } = render(
//         <BrowserRouter>
//         <AuthProvider>
//         <LinkAssets />
//         </AuthProvider>
//         </BrowserRouter>);
//     expect(container.querySelector('.crypto__image').alt).toEqual('#');
//   });
// });