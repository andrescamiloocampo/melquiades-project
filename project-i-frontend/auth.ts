import NextAuth from "next-auth";
import authConfig from "./auth.config";
import Credentials from "next-auth/providers/credentials";
import { getUserByName } from "./api/user/getUserByName";
import { z } from 'zod';
import * as bcrypt from 'bcrypt';
import { LoginUser } from "./api/auth/loginUser";

export const {handlers,auth,signIn,signOut} = NextAuth({
    session: {strategy: 'jwt'},
    ...authConfig,
    providers: [
        Credentials({
            credentials: {
                username: {},
                password: {},
            },
            // authorize: async (credentials:any):Promise<any> => {
            //     try {
            //         let user = null;

            //         const parsedCredentials = z.object({
            //             username:z.string(),
            //             password: z.string().min(8),
            //         }).safeParse(credentials);
                    
            //         const {username,password} = parsedCredentials.data as any;

            //         user = await getUserByName(credentials.username);   
                                        
            //         if(!user)
            //             throw new Error('User not found');                                                
                                
            //         const match = bcrypt.compareSync(password,user.password);

            //         if(!match) throw new Error('Invalid credentials');

            //         const session = await LoginUser(username,password);                            
            //         return {
            //             id: user.id,
            //             name: user.name,
            //             email: user.email,
            //             sessionData: session
            //         };

            //     } catch (error) {
            //         console.log(error);
            //         return null;
            //     }   
            // },
            authorize: async (credentials: any): Promise<any> => {
                try {
                    let user = null;
                    const parsedCredentials = z.object({
                        username: z.string(),
                        password: z.string().min(8),
                    }).safeParse(credentials);
            
                    if (!parsedCredentials.success) {
                        return { error: 'Invalid input format' };
                    }
            
                    const { username, password } = parsedCredentials.data;
                    user = await getUserByName(username);
            
                    if (!user) return { error: 'User not found' };
            
                    const match = bcrypt.compareSync(password, user.password);
                    if (!match) return { error: 'Invalid credentials' };
            
                    const session = await LoginUser(username, password);
            
                    return {
                        id: user.id,
                        name: user.name,
                        email: user.email,
                        sessionData: session,
                    };
                } catch (error: any) {
                    return { error: error.message };
                }
            }
              
        })
    ],
    callbacks: {
        async jwt({ token, user }: { token: any, user: any }) {
            if (user) {
                token.id = user.id;
                token.sessionData = user.sessionData;
            }
            if (user?.error) {
                token.error = user.error;
            }
            return token;
        },
        
        async session({ session, token }: { session: any, token: any }) {
            if (token) {
                session.user.id = token.id;
                session.user.sessionData = token.sessionData;
                if (token.error) {
                    session.error = token.error;  
                }
            }
            return session;
        }
    }
})