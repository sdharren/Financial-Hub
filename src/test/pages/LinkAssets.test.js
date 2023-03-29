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
    const debitText = screen.getByText("Link your bank account");
    const assetText = screen.getByText("Link your brokerage account");
    const cryptoText = screen.getByText("Link your crypto wallet");
    expect(debitText).toBeInTheDocument();
    expect(assetText).toBeInTheDocument();
    expect(cryptoText).toBeInTheDocument();

  })

  it("should render the images for the page", () => {
    customRenderUser(<LinkAssets />);
    const bankImg = screen.getByRole('img', {name : "debit_image"});
    const assetImg = screen.getByRole('img', {name : "stock_image"});
    const cryptoImg = screen.getByRole('img', {name : "crypto_image"});
    expect(bankImg['src']).toEqual("http://localhost/asset-debit2.png");
    expect(assetImg['src']).toEqual("http://localhost/asset-bank2.png");
    expect(cryptoImg['src']).toEqual("http://localhost/asset-crypto2.png");
    
  })

  
   
    const mockNavigate = jest.fn();
  
    const renderLinkAssets = () => {
      customRenderUser(<LinkAssets />)
    };
  
    it('renders LinkAssets component',  () => {
      renderLinkAssets();
      const linkAssetsComponent = screen.getByTestId('linkassetstest');
      expect(linkAssetsComponent).toBeInTheDocument();
    });
  
    
  
});