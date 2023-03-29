import React from 'react';
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { customRenderUser, customRenderNoUser} from '../test-utils'
import LinkAssets from "../../pages/LinkAssets";
import { Link } from 'react-router-dom';

describe("LinkAssets component", () => {
  it("should render correctly for a logged-in user", () => {
    customRenderUser(<LinkAssets />);
    expect(screen.getByTestId("linkassetstest")).toBeInTheDocument();
    expect(screen.getAllByRole("button")).toHaveLength(3);
  });

  it("should render texts for the page", () => {
    customRenderUser(<LinkAssets />);
    const debitText = screen.getByText("Link your credit or debit card");
    const assetText = screen.getByText("Link your brokerage account");
    const cryptoText = screen.getByText("Link your crypto wallet");
    expect(debitText).toBeInTheDocument();
    expect(assetText).toBeInTheDocument();
    expect(cryptoText).toBeInTheDocument();

  })

  it("should render the images for the page", () => {
    customRenderUser(<LinkAssets />);
    const bankImg = screen.getByRole('img', {name : "debit__card__image"});
    const assetImg = screen.getByRole('img', {name : "bank__image"});
    const cryptoImg = screen.getByRole('img', {name : "crypto__image"});
    expect(bankImg['src']).toEqual("http://localhost/asset-debit.png");
    expect(assetImg['src']).toEqual("http://localhost/asset-bank.png");
    expect(cryptoImg['src']).toEqual("http://localhost/asset-crypto.png");
    
  })

  it("should render the background images for the page", () => {
    customRenderUser(<LinkAssets />);
    const backgroundImg1 = screen.getByRole('img', { name: "background__image1"});
    const backgroundImg2 = screen.getByRole('img', { name: "background__image2"});
    const backgroundImg3 = screen.getByRole('img', { name: "background__image3"});
    expect(backgroundImg1['src']).toEqual("http://localhost/asset-background.png");
    expect(backgroundImg2['src']).toEqual("http://localhost/asset-background.png");
    expect(backgroundImg3['src']).toEqual("http://localhost/asset-background.png");
  });

  
   
    const mockNavigate = jest.fn();
  
    const renderLinkAssets = () => {
      customRenderUser(<LinkAssets />)
    };
  
    it('renders LinkAssets component',  () => {
      renderLinkAssets();
      const linkAssetsComponent = screen.getByTestId('linkassetstest');
      expect(linkAssetsComponent).toBeInTheDocument();
    });
  
    it('calls get_link_token function with transactions product when Link button on credit/debit card asset is clicked', async () => {
      const mockGetLinkToken = jest.fn();
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () =>
            Promise.resolve({
              link_token: 'testLinkToken',
            }),
          status: 200,
        })
      );
      
      customRenderUser(<LinkAssets />);

      const links = await screen.queryByTestId('linktransactions');
      fireEvent.click(links);

      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith(
          '/plaid_link',
          expect.objectContaining({
            state: expect.objectContaining({ link_token: 'mockToken' }),
          })
        );

        });


    });
  
    it('calls get_link_token function with investments product when Link button on brokerage account asset is clicked', async () => {
      const mockGetLinkToken = jest.fn();
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () =>
            Promise.resolve({
              link_token: 'testLinkToken',
            }),
          status: 200,
        })
      );
  
      customRenderUser(<LinkAssets />);
  
      const linkButton = screen.getByText('Link', { exact: false });
      fireEvent.click(linkButton);
  
      await expect(mockGetLinkToken).toHaveBeenCalledWith('investments');
    });
  
    it('navigates to /crypto_addresses when Link button on crypto wallet asset is clicked', () => {
      customRenderUser(<LinkAssets />);
  
      const linkButton = screen.getByText('Link', { exact: false });
      fireEvent.click(linkButton);
  
      expect(mockNavigate).toHaveBeenCalledWith('/crypto_addresses', { replace: true });
    });
  
});