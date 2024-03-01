import collections, math

from typing import Dict, List, Tuple

from util import Color, Sat, User, Vector3


def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    """Assign users to satellites respecting all constraints."""
    solution = {}
    color = {0:Color.A,1:Color.B,2:Color.C,3:Color.D}

    #first approach or brute force
    #assign all the colors, until it reaches the maximum color then go next

    allBeam = list(users.items())

    usersSeen = set()
    satToUsers = collections.defaultdict(list)

    for sat, satVector in sats.items():
        currentColor = 0
        userCount = 0
        withoutInterference = {}

        remainingUsers = []

        for i in range(len(allBeam)):
            currID = allBeam[i][0]
            if currID not in usersSeen:
                remainingUsers.append((allBeam[i]))

        #this is a dummy entry or fake entry to try to capture the last element, and we're going to
        #add the second to last element since we're comparing it.
        remainingUsers.append((allBeam[i-1])) 


        #thinking ahead here, maybe we can use a graph and map out all users that have angles that are greater than 10 near each other
        #
        # for i in range(len(allBeams)):
        #     for j in range(len(allBeams)):
        #         if i != j:
        #             angle = satVector.angle_between(allBeams[i],allBeams[j])

        #             if angle >= 10:
        #                 if allBeams[i] not in withoutInterference:
        #                     withoutInterference[allBeams[i]] = [allBeams[j]]
        #                 else:
        #                     withoutInterference[allBeams[i]].append(allBeams[j])

        #each satellite will attempt to get 32 userse
        #each user will be greater than 10 degrees
        #if less than, we assign a different color, and if we reach four, we skip it
        #then we reset count to 0 if we find another that has greater than 10 degrees
        #basic idea is satelliters will try grabbing all possible users, and then remaining satellite will do the rest
        

        #allBeam = (user,vector)
        left = 0
        for i in range(1,len(remainingUsers)):
            prevUserId = remainingUsers[left][0]
            prevUserVector = remainingUsers[left][1]
            currentUserId = remainingUsers[i][0]
            currentUserVector = remainingUsers[i][1]

            if userCount > 32:
                break

            angle = satVector.angle_between(prevUserVector,currentUserVector)

            visibleAngle = math.degrees(math.acos(prevUserVector.unit().dot((satVector - prevUserVector).unit())))

            #check if angle is less than 10
            if 0 <= visibleAngle <= 45:
                if angle < 10:
                    # if less than 10 and currentcolor is less than 4, try grab userß
                    if 0 <= currentColor < 4:
                        satToUsers[sat].append((prevUserId,color[currentColor]))
                        currentColor += 1
                    else:
                        continue
                else:
                    if 0 <= currentColor <= 3:
                        satToUsers[sat].append((prevUserId,color[currentColor]))
                    elif currentColor == 4:
                        satToUsers[sat].append((prevUserId,color[currentColor-1]))
                

            userCount += 1

            #keep track of the previous so we dont reach the color limit
            left = i
    

    for key,value in sorted(satToUsers.items(), key = lambda x: len(x[1]), reverse=True):
        sat = key
        for i in range(len(value)):
            user = value[i][0]
            color = value[i][1]
            if user not in usersSeen:
                solution[user] = (sat,color)
                usersSeen.add(user)

    # TODO: Implement.
                

    return solution



