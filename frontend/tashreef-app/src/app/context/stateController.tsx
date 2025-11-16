"use client";
import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  route: string;
}

interface CardResponse {
  card_svg: string;
  pattern_config: any;
  content_config: any;
}

interface StateControllerState {
  navItems: NavItem[];
  setNavItems: (items: NavItem[]) => void;
  cardResponse: CardResponse | null;
  setCardResponse: (response: CardResponse | null) => void;
}

const StateControllerContext = createContext<StateControllerState | undefined>(undefined);

export const StateControllerProvider = ({ children }: { children: ReactNode }) => {
  const [sessionData, setSessionData] = useState<any>(null);
  const [navItems, setNavItems] = useState<NavItem[]>([]);
  const [cardResponse, setCardResponse] = useState<CardResponse | null>(null);

  useEffect(() => {
    const loadSessionData = async () => {

    };

    loadSessionData();
  }, []);

  return (
    <StateControllerContext.Provider value={{
      navItems,
      setNavItems,
      cardResponse,
      setCardResponse,
    }}>
      {children}
    </StateControllerContext.Provider>
  );
};

export const useStateController = () => {
  const context = useContext(StateControllerContext);
  if (context === undefined) {
    throw new Error('useStateController must be used within a StateControllerProvider');
  }
  return context;
};
