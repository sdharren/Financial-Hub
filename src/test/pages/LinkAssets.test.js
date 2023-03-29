import React from 'react';
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { customRenderUser, customRenderNoUser} from '../test-utils'
import LinkAssets from "../../pages/LinkAssets";

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

  // it("should render the background images for the page", () => {
  //   customRenderUser(<LinkAssets />);
  //   const backgroundImg1 = screen.getByRole('img', { name: "background__image1"});
  //   const backgroundImg2 = screen.getByRole('img', { name: "background__image2"});
  //   const backgroundImg3 = screen.getByRole('img', { name: "background__image3"});
  //   expect(backgroundImg1['src']).toEqual("http://localhost/asset-background.png");
  //   expect(backgroundImg2['src']).toEqual("http://localhost/asset-background.png");
  //   expect(backgroundImg3['src']).toEqual("http://localhost/asset-background.png");
  // });

  it("should navigate to the crypto addresses page when clicking on the crypto wallet button", async () => {
    customRenderUser(<LinkAssets />);
    const linkButton = screen.getAllByText("Link")[2];
    fireEvent.click(linkButton);
    expect(screen.getByText("Link your crypto wallet"));
  });
});