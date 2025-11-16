"use client";
import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  route: string;
}

interface StateControllerState {

  // new
  navItems: NavItem[];
  setNavItems: (items: NavItem[]) => void;


}

const StateControllerContext = createContext<StateControllerState | undefined>(undefined);

export const StateControllerProvider = ({ children }: { children: ReactNode }) => {
  const [sessionData, setSessionData] = useState<any>(null);

  //new
  const [navItems, setNavItems] = useState<NavItem[]>([]);
  // Load session data when currentSessionGuid changes
  useEffect(() => {
    const loadSessionData = async () => {

    };

    loadSessionData();
  }, []);

  return (
    <StateControllerContext.Provider value={{
      // new
      navItems,
      setNavItems,
      
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
